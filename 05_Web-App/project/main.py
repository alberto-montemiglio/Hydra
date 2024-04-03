from flask import Blueprint, render_template
from flask_login import login_required, current_user
from bokeh.resources import INLINE
from bokeh.embed import components
from . import water_intake_page, water_intake_monitor_page, water_intake_analysis_page



main = Blueprint('main', __name__)


# Index Page Route:

@main.route('/') 
def index():
    return render_template('index.html')


# Water Intake Route, with login required:

@main.route('/waterIntake')
@login_required
def waterIntake():
    
    fig = water_intake_page.water_intake_page()
    script, div = components(fig)

    return render_template(
        'waterIntake.html',
        name=current_user.name,
        plot_script=script,
        plot_div=div,
        js_resources=INLINE.render_js(),
        css_resources=INLINE.render_css(),
    ).encode(encoding='UTF-8')


# Water Intake Analysis Route, with login required:

@main.route('/waterIntakeAnalysis')
@login_required
def waterIntakeAnalysis():

    p_trend, p_season, p_resid = water_intake_analysis_page.water_intake_analysis_page()
    
    script_p_trend, div_p_trend = components(p_trend)
    script_p_season, div_p_season = components(p_season)
    script_p_resid, div_p_resid = components(p_resid)


    return render_template(
        'waterIntakeAnalysis.html',
        name=current_user.name,
        script_p_trend=script_p_trend,
        div_p_trend=div_p_trend,
        script_p_season=script_p_season,
        div_p_season=div_p_season,
        script_p_resid=script_p_resid,
        div_p_resid=div_p_resid,
        js_resources=INLINE.render_js(),
        css_resources=INLINE.render_css(),
    ).encode(encoding='UTF-8')


# Water Intake Monitoring Route, with login required:

@main.route('/waterIntakeMonitoring')
@login_required
def waterIntakeMonitoring():

    progress, onTrack = water_intake_monitor_page.water_intake_monitor_page(current_user.weight, current_user.height, current_user.age)
    
    return render_template(
        'waterIntakeMonitor.html',
        name=current_user.name,
        progress=progress,
        onTrack = onTrack
    ).encode(encoding='UTF-8')



if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)
