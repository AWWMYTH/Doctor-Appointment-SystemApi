from flask import Flask, jsonify, request

app = Flask(__name__)

# Sample data (replace with a database in a real application)
doctors = [
    {"id": 1, "name": "Dr. Smith", "schedule": "Evenings", "max_patients": 10},
    {"id": 2, "name": "Dr. Johnson", "schedule": "Evenings", "max_patients": 8},
    # Add more doctors as needed
]

appointments = []


@app.route('/doctors', methods=['GET'])
def get_doctors():
    return jsonify(doctors)


@app.route('/doctors/<int:doctor_id>', methods=['GET'])
def get_doctor_detail(doctor_id):
    doctor = next((d for d in doctors if d["id"] == doctor_id), None)
    if doctor:
        return jsonify(doctor)
    else:
        return jsonify({"error": "Doctor not found"}), 404


@app.route('/appointments', methods=['POST'])
def book_appointment():
    data = request.get_json()
    doctor_id = data.get("doctor_id")
    patient_name = data.get("patient_name")

    doctor = next((d for d in doctors if d["id"] == doctor_id), None)
    if not doctor:
        return jsonify({"error": "Doctor not found"}), 404

    if len(appointments) >= doctor["max_patients"]:
        return jsonify({"error": "No available appointments"}), 400

    appointment = {
        "doctor_id": doctor_id,
        "patient_name": patient_name,
    }
    appointments.append(appointment)

    return jsonify({"message": "Appointment booked successfully"})


if __name__ == '__main__':
    app.run(debug=True)
