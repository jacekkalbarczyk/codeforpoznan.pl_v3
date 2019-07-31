from http import HTTPStatus

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from flask_restful import Resource

from backend.models import Participant
from backend.serializers.participant_serializer import (
    participant_schema, participants_schema
)


class ParticipantsList(Resource):
    @jwt_required
    def get(self):
        participants_list = Participant.query.all()
        if participants_list:
            participants = participants_schema.dump(participants_list)
            return {"participants": participants}, 200
        return {"message": "Participants not found"}, 404


class ParticipantDetails(Resource):
    @jwt_required
    def get(self, id):
        return participant_schema.dump(
            Participant.query.get_or_404(id)
        ), HTTPStatus.OK
