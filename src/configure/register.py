from main import (
    access_data, access_menu, app_data, branch, consumer,
    data_chart, data_load, data_report, profile, vendor
)
from utils import security_user

def register_blueprints(app):
    app.register_blueprint(security_user.blueprint)
    app.register_blueprint(access_data.blueprint)
    app.register_blueprint(access_menu.blueprint)
    app.register_blueprint(app_data.blueprint)
    app.register_blueprint(branch.blueprint)
    app.register_blueprint(consumer.blueprint)
    app.register_blueprint(data_chart.blueprint)
    app.register_blueprint(data_load.blueprint)
    app.register_blueprint(data_report.blueprint)
    app.register_blueprint(profile.blueprint)
    app.register_blueprint(vendor.blueprint)
