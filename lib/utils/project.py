from lib.ressources.models import ProjectDetails


def project_path(request: ProjectDetails):
    name = f"{request.basicat}-{request.workload_details}-{request.env}"
    env = request.env
    return f"prod/{name}"


def name(request: ProjectDetails):
    coutry = request.country
    basicat = request.basicat
    workload = request.workload_details
    unicity = request.unicity_id
    env = request.env
    name = f"{coutry}-{basicat}-{workload}-{unicity}-{env}"
    return name
