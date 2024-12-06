# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 11:48:13 2024

@author: max
"""

from flask import Flask, request, jsonify
import random

app = Flask(__name__)

# Participant list
participants = ["Max", "Sam", "Adam", "Harry", "Robin"]
assignments = {name: None for name in participants}
available_names = set(participants)

@app.route("/spin", methods=["POST"])
def spin():
    global available_names, assignments
    data = request.json
    person = data.get("person")
    
    if person not in participants:
        return jsonify({"error": "Invalid person"}), 400

    # Ensure the person hasn't already spun
    if assignments[person] is not None:
        return jsonify({"message": "You already have an assignment", "assignment": assignments[person]})

    # Filter available names to avoid self-assignment
    valid_names = [name for name in available_names if name != person]

    if not valid_names:
        return jsonify({"error": "No valid names left"}), 400

    # Randomly assign a name
    chosen_name = random.choice(valid_names)
    assignments[person] = chosen_name
    available_names.remove(chosen_name)

    return jsonify({"message": f"You got {chosen_name}!"})

@app.route("/status", methods=["GET"])
def status():
    return jsonify({"assignments": assignments, "available_names": list(available_names)})

if __name__ == "__main__":
    app.run(debug=True)
