def route_pipeline(content_type: str):
    routes = {
        "code": "code_pipeline",
        "document": "text_pipeline",
        "slide": "summary_pipeline",
        "diagram": "visual_pipeline",
        "mixed": "hybrid_pipeline",
    }

    return routes.get(content_type, "hybrid_pipeline")
