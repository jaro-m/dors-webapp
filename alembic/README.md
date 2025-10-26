# WIP
## TODO:
Most endpoints should work now, but more validation is required.
The code for authentication/authorization is present, but not used for the endpoints yet.

## All endpoints
#   ----- ENDPOINTS ------
# POST    /api/reports                  # Create new report               +
# GET     /api/reports                  # List reports (paginated)        +
# GET     /api/reports/{id}             # Get specific report             +
# PUT     /api/reports/{id}             # Update report (draft only)      +
# DELETE  /api/reports/{id}             # Delete report (draft only)      +

# POST    /api/reports/{id}/reporter    # Add/update reporter details     +
# GET     /api/reports/{id}/reporter    # Get reporter details            +
# POST    /api/reports/{id}/patient     # Add/update patient details      +
# GET     /api/reports/{id}/patient     # Get patient details             +
# POST    /api/reports/{id}/disease     # Add/update disease details      +
# GET     /api/reports/{id}/disease     # Get disease details             +

# POST    /api/reports/{id}/submit      # Submit report (change status)   -
# GET     /api/reports/search           # Search reports                  -
# GET     /api/statistics               # Basic statistics                -

#   ----- ADVANCED -----
# GET     /api/reports/export/{format}  # Export data (CSV/JSON)          -
# GET     /api/diseases/categories      # Get disease categories          -
# GET     /api/reports/recent           # Recent submissions              -
