from flask import Blueprint, jsonify, abort, make_response, request
from app.models.planet import Planet
from app import db

planets_bp = Blueprint("planets_bp", __name__, url_prefix = "/planets")

# HELPER FUNCTION
def validate_id(class_obj, id):
    try:
        object_id = int(id)
    except:
        abort(make_response({"message":f"{class_obj} {id} is invalid"}, 400))
    
    query_result = class_obj.query.get(object_id)
    if not query_result:
        abort(make_response({"message":f"{class_obj} {id} is not found"}, 404))

    return query_result

# CREATE RESOURCE
@planets_bp.route("", methods = ["POST"])
def create_planet():
    request_body = request.get_json()
    
    new_planet = Planet.from_json(request_body)
        
    db.session.add(new_planet)
    db.session.commit()

    return make_response(f"Planet {new_planet.name} has been created", 201)


# GET ALL RESOURCES
@planets_bp.route("", methods = ["GET"])
def get_all_planets():
    results_list = []

    color_param= request.args.get("color")
    description_param= request.args.get("description")
    
    if color_param:
        planets = Planet.query.filter_by(color=color_param)
    elif description_param:
        planets = Planet.query.filter_by(description=description_param)
    else:
        planets = Planet.query.all()

    for planet in planets:
        results_list.append(planet.to_dict())
    
    return jsonify(results_list), 200


# GET ALL RESOURCES
@planets_bp.route("/<planet_id>", methods = ["GET"])
def get_one_planet(planet_id):
    planet = validate_id(Planet, planet_id)

    return jsonify(planet.to_dict())


# UPDATE RESOURCE
@planets_bp.route("/<planet_id>", methods = ["PUT"])
def update_planet(planet_id):
    planet = validate_id(Planet, planet_id)

    request_body = request.get_json()

    try:
        planet.update(request_body)
    except KeyError as error:
        return make_response({'message': f"Missing attribute: {error}"}, 400)

    db.session.commit()

    return make_response(f"planet {planet_id} successfully updated")


# DELETE RESOURCE
@planets_bp.route("/<planet_id>", methods = ["DELETE"])
def delete_planet(planet_id):
    planet = validate_id(Planet, planet_id)

    db.session.delete(planet)
    db.session.commit()

    return make_response(f"planet #{planet_id} successfully deleted")






# # class Planet:
# #     def __init__(self, id, name, color, description):
# #         self.id = id
# #         self.name = name
# #         self.color = color
# #         self.description = description

# # planets = [
# #     Planet(1, "Saturn", "yellowish-brown", "Saturn is the sixth planet from the Sun and the second-largest planet in our solar system."),
# #     Planet(2, "Mars", "rusty red", "Mars is the fourth planet from the Sun – a dusty, cold, desert world with a very thin atmosphere."),
# #     Planet(3, "Jupiter", "beige", "Jupiter is covered in swirling cloud stripes. It has big storms like the Great Red Spot, which has been going for hundreds of years. "),
# #     Planet(4, "Earth", "blue and green", "Earth is a rocky, terrestrial planet. It has a solid and active surface with mountains, valleys, canyons, plains and so much more."),
# #     Planet(5, "Venus", "beige", "It’s one of the four inner, terrestrial (or rocky) planets, and it’s often called Earth’s twin because it’s similar in size and density."),
# #     Planet(6, "Uranus", "blue", "Uranus is the seventh planet from the Sun, and has the third-largest diameter in our solar system."),
# #     Planet(7, "Neptune", "blue", "Dark, cold, and whipped by supersonic winds, ice giant Neptune is the eighth and most distant planet in our solar system"),
# #     Planet(8, "Pluto", "off-white and light blue", "Pluto is a dwarf planet in the Kuiper Belt, a donut-shaped region of icy bodies beyond the orbit of Neptune."),
# #     Planet(9, "Mercury", "dark gray", "Mercury—the smallest planet in our solar system and closest to the Sun—is only slightly larger than Earth's Moon.")


# # ]

# # planets_bp = Blueprint("planets_bp", __name__, url_prefix = "/planets")

# # @planets_bp.route("", methods = ["GET"])
# # def get_all_planets():
# #     planets_response = []
# #     for planet in planets:
# #         planets_response.append(
# #         {"id": planet.id,
# #             "name": planet.name,
# #             "color": planet.color,
# #             "description": planet.description
#         }
#         )
#     return jsonify(planets_response)




# @planets_bp.route("/<id>", methods = ["GET"])
# def get_one_planet(id):
    # try:
    #     planet_id = int(id)
    # except:
    #     abort(make_response({"message":f"Planet {id} is invalid"}, 400))
    
    # planet = int(id)
    # for planet in planets:
    #     if planet.id == planet_id:
    # planet = validate_planet_id(id)
    # return (
    #     {"id": planet.id,
    #         "name": planet.name,
    #         "color": planet.color,
    #         "description": planet.description
    #     }
    # )
        
