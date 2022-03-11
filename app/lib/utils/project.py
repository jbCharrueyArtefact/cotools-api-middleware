def project_path(request):
    name = f"{request.basicat}-{request.workload_details}-{request.env}"
    return f"prod/{name}"


def create_name(request):
    coutry = request.country
    basicat = request.basicat
    workload = request.workload_details
    unicity = request.unicity_id
    env = request.env
    if not unicity:
        name = f"{coutry}-{basicat}-{workload}-{env}"
    else:
        name = f"{coutry}-{basicat}-{workload}-{unicity}-{env}"
    return name
