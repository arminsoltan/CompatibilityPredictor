from flask import Flask, request
from flask_restful import Resource, Api
import numpy as np

app = Flask(__name__)
api = Api(app)

class Compatibility(Resource):
    def post(self):
        data = request.get_json()
        team_members = data["team"]
        applicants = data["applicants"]
        result = self.calculate_applicant_score(applicants, team_members)
        return result

    def calculate_applicant_score(self, applicants, team_members):
        result = {
            "scoredApplicants": list()
        }
        for applicant in applicants:
            applicant_att_vec = self.get_attributes_vector(applicant["attributes"])
            applicant_score = 0
            for member in team_members:
                member_att_vec = self.get_attributes_vector(member["attributes"])
                applicant_score += self.calculate_similarity_applicant_with_team_member(applicant_att_vec, member_att_vec)        
            applicant_score = applicant_score / len(team_members)
            result["scoredApplicants"].append({
                "name": applicant["name"],
                "score": applicant_score
            })
        return result
        
    @staticmethod
    def get_attributes_vector(attributes):
        intelligence = int(attributes.get("intelligence", 0))
        strength = int(attributes.get("strength", 0))
        endurance = int(attributes.get("endurance", 0))
        spicyFoodTolerance = int(attributes.get("spicyFoodTolerance", 0))
        return np.array([intelligence, strength, endurance, spicyFoodTolerance])
    
    @staticmethod
    def calculate_similarity_applicant_with_team_member(applicant_att_vec, member_att_vec):
        return np.dot(applicant_att_vec, member_att_vec) / (np.linalg.norm(applicant_att_vec) * np.linalg.norm(member_att_vec))
    
api.add_resource(Compatibility, "/compatibility")

if __name__ == "__main__":
    app.run(debug=True)