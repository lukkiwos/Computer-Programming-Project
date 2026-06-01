from flask import Blueprint, request, render_template, jsonify
from extensions import db
from models import Game
from services.igdb_service import search_games
import datetime
from flask import redirect, flash

main = Blueprint("main", __name__)



@main.route("/", methods=["GET"])
def home():
    from flask import request
    import datetime

    name = request.args.get("name")
    sort = request.args.get("sort", "rating")
    order = request.args.get("order", "desc")

    games = []

    if name:
        games = search_games(name)

        for g in games:
            if "first_release_date" in g:
                g["first_release_date"] = datetime.datetime.fromtimestamp(
                    g["first_release_date"]
                ).strftime("%Y-%m-%d")

    if sort == "rating":
        games.sort(key=lambda x: x.get("rating", 0), reverse=(order == "desc"))

    elif sort == "name":
        games.sort(key=lambda x: x.get("name", ""), reverse=(order == "desc"))

    elif sort == "date":
        games.sort(key=lambda x: x.get("first_release_date", ""), reverse=(order == "desc"))

    return render_template("index.html", games=games)


@main.route("/add-game", methods=["POST"])
def add_game():
    igdb_id = request.form.get("igdb_id")
    name = request.form.get("name")
    rating = request.form.get("rating")
    release_date = request.form.get("release_date")

    existing = Game.query.filter_by(igdb_id=igdb_id).first()

    if existing:
        flash("Gra już jest w Twojej kolekcji ⚠️")
    else:
        game = Game(
            igdb_id=igdb_id,
            name=name,
            rating=float(rating) if rating else None,
            release_date=release_date if release_date else None
        )
        db.session.add(game)
        db.session.commit()

        flash("Dodano grę do kolekcji ✅")

    return redirect(request.referrer or "/")


@main.route("/my-games")
def my_games():
    search = request.args.get("search")
    sort = request.args.get("sort")
    order = request.args.get("order", "desc")  # domyślnie malejąco

    query = Game.query

    if search:
        query = query.filter(Game.name.ilike(f"%{search}%"))

    if sort == "rating":
        if order == "asc":
            query = query.order_by(Game.rating.asc())
        else:
            query = query.order_by(Game.rating.desc())

    elif sort == "name":
        if order == "asc":
            query = query.order_by(Game.name.asc())
        else:
            query = query.order_by(Game.name.desc())

    elif sort == "date":
        if order == "asc":
            query = query.order_by(Game.release_date.asc())
        else:
            query = query.order_by(Game.release_date.desc())

    games = query.all()

    return render_template("my_games.html", games=games)


@main.route("/delete-game/<int:id>", methods=["POST"])
def delete_game(id):
    game = Game.query.get(id)

    if game:
        db.session.delete(game)
        db.session.commit()

    return redirect("/my-games")


@main.route("/api/games", methods=["GET"])
def api_get_games():
    games = Game.query.all()
    games_list = []
    for g in games:
        games_list.append({
            "id": g.id,
            "igdb_id": g.igdb_id,
            "name": g.name,
            "rating": g.rating,
            "release_date": g.release_date
        })
    return jsonify({"status": "success", "data": games_list}), 200


@main.route("/api/games/<int:id>", methods=["PUT"])
def api_update_game(id):
    game = Game.query.get(id)
    if not game:
        return jsonify({"status": "error", "message": "Gra nie znaleziona"}), 404

    data = request.get_json()
    
    if "rating" in data:
        game.rating = data["rating"]
        db.session.commit()
        return jsonify({"status": "success", "message": "Zaktualizowano ocenę"}), 200
        
    return jsonify({"status": "error", "message": "Brak danych do aktualizacji"}), 400