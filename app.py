from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"student_number": "123456789"})  # Replace with yours

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json()
    intent = req["queryResult"]["intent"]["displayName"]

    if intent == "BudgetTripPlanning":
        params = req["queryResult"]["parameters"]
        destination = params.get("geo-country", "the selected destination")
        duration = int(params.get("duration", 0))
        budget = params.get("budget", {}).get("amount", 0)

        # Basic cost estimation
        flight_cost = 300
        hotel_per_night = 50
        extras = 100

        total_cost = flight_cost + (hotel_per_night * duration) + extras

        if total_cost <= budget:
            message = (
                f"Great! A {duration}-day trip to {destination} under ${budget} is totally doable. "
                f"Estimated cost is around ${total_cost}. Let me know if you'd like help booking it!"
            )
        else:
            message = (
                f"Hmm, a {duration}-day trip to {destination} might exceed your ${budget} budget. "
                f"Estimated cost is around ${total_cost}. Want to adjust your duration or pick a cheaper destination?"
            )

        return jsonify({"fulfillmentText": message})

    return jsonify({"fulfillmentText": "Sorry, I couldn't process your request."})

if __name__ == '__main__':
    app.run(debug=True)
    