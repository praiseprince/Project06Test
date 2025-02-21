from flask import Blueprint, jsonify, request, abort
from ..db_models import db, Item
from ..auth import basic_auth_required

api_bp = Blueprint('api', __name__, url_prefix='/api')

def item_to_dict(item):
    return {
        "id": item.id,
        "name": item.name,
        "price": item.price,
        "category": item.category,
        "details": item.details,
        "image": item.image,
        "price_id": item.price_id,
    }

# GET all items (open to everyone)
@api_bp.route('/items', methods=['GET'])
def get_items():
    items = Item.query.all()
    return jsonify([item_to_dict(item) for item in items]), 200

# GET a single item (open to everyone)
@api_bp.route('/item/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = Item.query.get_or_404(item_id)
    return jsonify(item_to_dict(item)), 200

# POST a new item (admin only)
@api_bp.route('/items', methods=['POST'])
@basic_auth_required
def create_item():
    data = request.get_json()
    if not data or 'name' not in data or 'price' not in data:
        return jsonify({"error": "Invalid data. 'name' and 'price' are required."}), 400

    new_item = Item(
        name=data.get("name"),
        price=data.get("price"),
        category=data.get("category", ""),
        details=data.get("details", ""),
        image=data.get("image", ""),
        price_id=data.get("price_id", "")
    )
    db.session.add(new_item)
    db.session.commit()
    return jsonify({"message": "Item created", "item": item_to_dict(new_item)}), 201

# PATCH to update an item (admin only)
@api_bp.route('/item/<int:item_id>', methods=['PATCH'])
@basic_auth_required
def update_item(item_id):
    item = Item.query.get_or_404(item_id)
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided for update."}), 400

    if "price" in data:
        item.price = data["price"]
    if "name" in data:
        item.name = data["name"]
    if "category" in data:
        item.category = data["category"]
    if "details" in data:
        item.details = data["details"]
    if "image" in data:
        item.image = data["image"]
    if "price_id" in data:
        item.price_id = data["price_id"]

    db.session.commit()
    return jsonify({"message": "Item updated", "item": item_to_dict(item)}), 200

# DELETE an item (admin only)
@api_bp.route('/item/<int:item_id>', methods=['DELETE'])
@basic_auth_required
def delete_item(item_id):
    item = Item.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({"message": "Item deleted"}), 200

# OPTIONS endpoint for /items (open to everyone)
@api_bp.route('/items', methods=['OPTIONS'])
def items_options():
    response = jsonify({"allowed_methods": ["GET", "POST", "OPTIONS"]})
    response.headers["Allow"] = "GET, POST, OPTIONS"
    return response, 200

# OPTIONS endpoint for /item/<item_id> (open to everyone)
@api_bp.route('/item/<int:item_id>', methods=['OPTIONS'])
def item_options(item_id):
    response = jsonify({"allowed_methods": ["GET", "PATCH", "DELETE", "OPTIONS"]})
    response.headers["Allow"] = "GET, PATCH, DELETE, OPTIONS"
    return response, 200

@api_bp.route('/item/<int:item_id>', methods=['PUT'])
@basic_auth_required
def replace_item(item_id):
    """
    Fully replace an existing item. Requires all fields to be provided.
    """
    item = Item.query.get_or_404(item_id)
    data = request.get_json()
    
    if not data or 'name' not in data or 'price' not in data:
        return jsonify({"error": "Invalid data. 'name' and 'price' are required for full replacement."}), 400

    item.name = data.get("name")
    item.price = data.get("price")
    item.category = data.get("category", "")
    item.details = data.get("details", "")
    item.image = data.get("image", "")
    item.price_id = data.get("price_id", "")

    db.session.commit()
    return jsonify({"message": "Item fully replaced", "item": item_to_dict(item)}), 200
