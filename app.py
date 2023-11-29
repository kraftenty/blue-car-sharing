import data.initializer
import routes
import manager_auth_router
import manager_managemodel_router
import manager_managezone_router
import manager_managesubscription_router
import manager_managecar_router
import manager_managerepairment_router
import manager_managereservation_router
import manager_viewincome_router
import manager_manageuser_router
import user_auth_router
import user_findcar_router
import user_smartkey_router
import user_subscription_router
from flask import Flask
app = Flask(__name__)
app.secret_key = '1234'

data.initializer.initialize()


# Blueprint registration
app.register_blueprint(routes.main_bp)
app.register_blueprint(manager_auth_router.manager_auth_bp)
app.register_blueprint(manager_managemodel_router.manager_managemodel_bp)
app.register_blueprint(manager_managezone_router.manager_managezone_bp)
app.register_blueprint(manager_managesubscription_router.manager_managesubscription_bp)
app.register_blueprint(manager_managecar_router.manager_managecar_bp)
app.register_blueprint(manager_managerepairment_router.manager_managerepairment_bp)
app.register_blueprint(manager_managereservation_router.manager_managereservation_bp)
app.register_blueprint(manager_manageuser_router.manager_manageuser_bp)
app.register_blueprint(manager_viewincome_router.manager_viewincome_bp)
app.register_blueprint(user_auth_router.user_auth_bp)
app.register_blueprint(user_findcar_router.user_findcar_bp)
app.register_blueprint(user_smartkey_router.user_smartkey_bp)
app.register_blueprint(user_subscription_router.user_subscription_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True, port=5500)
