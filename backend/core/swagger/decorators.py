from drf_spectacular.utils import extend_schema


def api_schema(
    summary: str,
    description: str = "",
    request=None,
    response=None,
    tags=None,
    auth_required=True,
):
    # Decorator base para padronizar documentação Swagger.

    responses = {}

    if response:
        responses = {
            200: response,
            201: response,
        }

    return extend_schema(
        summary=summary,
        description=description,
        request=request,
        responses=responses,
        tags=tags or [],
    )


def professor_endpoint(
    summary,
    description="",
    request=None,
    response=None,
    tags=None,
):
    return api_schema(
        summary=f"{summary}",
        description=description,
        request=request,
        response=response,
        tags=tags or ["Professor"],
        auth_required=True,
    )


def aluno_endpoint(
    summary,
    description="",
    request=None,
    response=None,
    tags=None,
):
    return api_schema(
        summary=f"[ALUNO] {summary}",
        description=description,
        request=request,
        response=response,
        tags=tags or ["Aluno"],
        auth_required=True,
    )


def publico_endpoint(
    summary,
    description="",
    request=None,
    response=None,
    tags=None,
):
    return api_schema(
        summary=summary,
        description=description,
        request=request,
        response=response,
        tags=tags or ["Geral"],
        auth_required=True,
    )