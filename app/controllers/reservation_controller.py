from app.models.reservation_model import Reservation
from flask import Blueprint, request, jsonify
from app.views.reservation_view import render_reservation_detail,render_reservation_list
from app.utils.decorators import jwt_required, roles_required

reservation_bp = Blueprint("reservation", __name__)

@reservation_bp.route("/reservations", methods=["GET"])
@jwt_required
@roles_required(role=["Admin","customer"])
def get_reservations():
    reservations = Reservation.get_all()
    return jsonify(render_reservation_list(reservations)), 200

@reservation_bp.route("/reservations/<int:id>", methods=["GET"])
@jwt_required
@roles_required(role=["admin","customer"])
def get_reservation(id):
    reservation = Reservation.get_by_id(id)
    if reservation is None:
        return jsonify({"message": "Reserva no encontrada"}), 404
    return jsonify(render_reservation_detail(reservation)), 200

@reservation_bp.route("/reservations", methods=["POST"])
@jwt_required
@roles_required(role=["admin"])
def create_reservation():
    data = request.json
    user_id = data.get("user_id")
    restaurant_id = data.get("restaurant_id")
    reservation_date = data.get("reservation_date")
    num_guests = data.get("num_guests")
    special_request = data.get("special_request")
    status = data.get("status")
    
    if not user_id or not restaurant_id or not reservation_date or not num_guests or not status:
        return jsonify({"error": "Faltan datos requeridos"}), 400
    reservation = Reservation(user_id, restaurant_id, reservation_date, num_guests, special_request, status)
    reservation.save()
    return jsonify(render_reservation_detail(reservation)), 201

@reservation_bp.route("/reservations/<int:id>", methods=["PUT"])
@jwt_required
@roles_required(role=["admin"])
def update_reservation(id):
    reservation = Reservation.get_by_id(id)
    if not reservation:
        return jsonify({"error": "Reserva no encontrada"}), 404
    data = request.json
    user_id = data.get("user_id")
    restaurant_id = data.get("restaurant_id")
    reservation_date = data.get("reservation_date")
    num_guests = data.get("num_guests")
    special_request = data.get("special_request")
    status = data.get("status")
    
    reservation.update(user_id=user_id, restaurant_id=restaurant_id, reservation_date=reservation_date, num_guests=num_guests, special_request=special_request, status=status)
    return jsonify(render_reservation_detail(reservation)), 200

@reservation_bp.route("/reservations/<int:id>", methods=["DELETE"])
@jwt_required
@roles_required(role=["admin"])
def delete_reservation(id):
    reservation = Reservation.get_by_id(id)
    if not reservation:
        return jsonify({"error": "Reserva no encontrada"}), 404
    reservation.delete()
    return jsonify({"message": "Reserva eliminada"}), 200

