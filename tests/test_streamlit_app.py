from streamlit.testing.v1 import AppTest


def test_streamlit_app_renders_deterministic_report():
    app = AppTest.from_file("app/streamlit_app.py")

    app.run(timeout=10)

    assert not app.exception
    assert app.title[0].value == "ResearchGraphOS"
    assert any(item.value == "Short Answer" for item in app.subheader)
    assert any(item.value == "Recommended Next Steps" for item in app.subheader)
