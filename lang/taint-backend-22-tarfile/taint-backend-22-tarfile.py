import sys
import tarfile
import tempfile
from flask import Flask, request

app = Flask(__name__)

@app.route("/extract/<filename>")
def unsafe_archive_handler(filename):
    tar = tarfile.open(filename)
    # ruleid: taint-backend-22-tarfile
    tar.extract(path=tempfile.mkdtemp())
    tar.close()

@app.route("/extract")
def managed_members_archive_handler():
    filename = request.args.get("filename")
    tar2 = tarfile.open(filename)

    result = []
    for member in tar2.getmembers():
        if '../' in member.name:
            print('Member name container directory traversal sequence')
            continue
        elif (member.issym() or member.islnk()) and ('../' in member.linkname):
            print('Symlink to external resource')
            continue
        result.append(member)
    
    # todook: taint-backend-22-tarfile
    tar2.extractall(path=tempfile.mkdtemp(), members=result)
    tar2.close()


@app.route("/extract2")
def list_members_archive_handler():
    filename = request.args.get("filename")
    tar3 = tarfile.open(filename)
    # ruleid: taint-backend-22-tarfile
    tar3.extractall(path=tempfile.mkdtemp(), members=[])
    tar3.close()

@app.route("/extract2")
def provided_members_archive_handler():
    filename = request.args.get("filename")
    tar4 = tarfile.open(filename)
    # ruleid: taint-backend-22-tarfile
    tar4.extractall(path=tempfile.mkdtemp(), members=tar4)
    tar4.close()

# This test case is incorrect
# tarFile variable doesn't has getmembers method
# need to fix this!!
@app.route("/extract/tar/<tarfile>")
def members_filter(tarfile):
    result = []
    for member in tarfile.getmembers():
        if '../' in member.name:
            print('Member name container directory traversal sequence')
            continue
        elif (member.issym() or member.islnk()) and ('../' in member.linkname):
            print('Symlink to external resource')
            continue
        result.append(member)
    return result


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        unsafe_archive_handler(filename)
        managed_members_archive_handler(filename)

@app.route("/extract3")
def untar_layers():
    output = {}
    filename = request.args.get('filename')
    # Untar layer filesystem bundle
    for layer in layers:
        tarfile = TarFile(filename)
        for member in tarfile.getmembers():
            try:
                # ruleid: taint-backend-22-tarfile
                tarfile.extract(member, path=dir, set_attrs=False)
            except (ValueError, ReadError) as ex:
                if InternalServer.is_debug_logging_enabled():
                    message = "Unexpected exception of type {0} occurred while untaring the docker image: {1!r}" \
                        .format(type(ex).__name__, ex.get_message() if type(ex).__name__ == 'DagdaError' else ex.args)
                    DagdaLogger.get_logger().debug(message)
            except PermissionError as ex:
                message = "Unexpected error occurred while untaring the docker image: " + \
                          "Operation not permitted on {0!r}".format(member.name)
                DagdaLogger.get_logger().warn(message)

    # Clean up
    for layer in layers:
        clean_up(dir + "/" + layer[:-10])