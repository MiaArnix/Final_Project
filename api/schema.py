from rest_framework.schemas.openapi import AutoSchema

# adjustment in AutoSchema to require Bearer token for all endpoints
class JWTBearerAutoSchema(AutoSchema):
    def get_components(self, path, method):
        components = super().get_components(path, method)
        
        if method in ["POST", "PUT", "PATCH", "DELETE"]:
            components.setdefault("securitySchemes", {})
            components["securitySchemes"]["BearerAuth"] = {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT",
                "description": "Use Authorization header: Bearer <access_token>",
            }
        return components

    def get_security(self, path, method):
        security = super().get_security(path, method) or []
        bearer_requirement = {"BearerAuth": []}
        if method in ["POST", "PUT", "PATCH", "DELETE"] and bearer_requirement not in security:
            security.append(bearer_requirement)
        return security