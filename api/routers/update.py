import jsonref
from fastapi import APIRouter
from msys.core.generators.open_api.OOP_generator.oopgenerator import \
    OOPGenerator
# from msys.core.generators.open_api.deployer import Deployer
from shared_data import shared_queue, update_event

router = APIRouter()


@router.put("/")
async def put_update(spec: dict):
    deref_spec = jsonref.JsonRef.replace_refs(spec)

    if deref_spec is None:
        return {"message": "Spec is empty"}

    if "openapi" in deref_spec:
        if deref_spec["openapi"].startswith("3.0"):
            generator = OOPGenerator(deref_spec)
            generator.generate_client_file_obj()
            # generator.generate_client_code()

            # deployer = Deployer(generator)
            # deployer.deploy_clients()
            shared_queue.put(
                generator)  # Put the generator object into the queue
            update_event.set()  # Set the event to notify the UI thread
            return {"message": "REST Interfaces updated"}
        else:
            print("Only OpenAPI 3.0.x is supported")
    elif "asyncapi" in deref_spec:
        print("AsyncAPI")
    else:
        return {"message": "Invalid spec"}

    return {"message": "Interfaces not updated"}
