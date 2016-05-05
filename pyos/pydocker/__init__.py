import time
from pyos.pyos.operation import SysOperation


class Docker(object):
    def __init__(self):
        self.os = SysOperation

    def rmi(self, image, *args, **kwargs):
        if self.image_exist(image):
            err, msg = self.os.run("docker rmi -f {0}".format(image))
            return not err
        else:
            return True

    def rmi_force(self, image, *args, **kwargs):
        for container in self.ps():
            if image in container:
                container_name = [_container for _container in container.split("\t") if _container][-1]
                self.stop(self.os.string_clean(container_name))

        time.sleep(5)
        for container in self.ps(a=True):
            if image in container:
                container_name = [_container for _container in container.split("\t") if _container][-1]
                self.rm(self.os.string_clean(container_name))

        time.sleep(3)
        return self.rmi(image)

    def rm(self, container, force=False, *args, **kwargs):
        if force:
            self.stop(container)
        if self.container_exist(container, False):
            err, msg = self.os.run("docker rm {0}".format(container))
            return not err
        else:
            return True

    def stop(self, container, *args, **kwargs):
        if self.container_exist(container, True):
            err, msg = self.os.run("docker stop {0}".format(container))
            return not err
        else:
            return True

    def run(self, image, container, links={}, volumes={},volumes_from=[],
            dns=[], command="", detach=True, expose={}, *args, **kwargs):

        link_str = ""
        volume_str = ""
        dns_str = ""
        volumes_from_str = ""
        expose_str = ""

        detach_str = "-d" if detach else ""
        for link in links.items():
            link_str += " --link {0}:{1} ".format(link[0], link[1])
        for volume in volumes.items():
            volume_str += " -v \"{0}\":\"{1}\" ".format(volume[0], volume[1])
        for _dns in dns:
            dns_str += " --dns {0} ".format(_dns)
        for volume_from in volumes_from:
            volumes_from_str += " --volumes-from {0} ".format(volume_from)
        for _expose in expose.items():
            expose_str += " -p {0}:{1} ".format(_expose[0], _expose[1])

        cmd = "docker run --name {0} {1} {2} {3} {4} {5} {6} {7} {8}".format(
              container, detach_str, link_str, volumes_from_str, volume_str, dns_str, expose_str, image, command)

        err, msg = self.os.run(cmd)
        return not err

    def start(self, container, *args, **kwargs):
        err, msg = self.os.run("docker start {0}".format(container))
        return not err

    def pull(self, images, *args, **kwargs):
        err, msg = self.os.run("docker pull {0}".format(images))
        return not err

    def tag(self, old_name, new_name, force=False, *args, **kwargs):
        err, msg = self.os.run("docker tag {0} {1} {2}".format("-f" if force else "", old_name, new_name))
        return not err

    def ps(self, a=False, *args, **kwargs):
        err, msg = self.os.run("docker ps {0}".format("-a" if a else ""))
        if err:
            return []
        else:
            return msg

    def images(self, a=False, *args, **kwargs):
        err, msg = self.os.run("docker images {0}".format("-a" if a else ""))
        return not err

    def restart(self, container, *args, **kwargs):
        err, msg = self.os.run("docker restart {0}".format(container))
        return not err

    def clear_containers(self, *args, **kwargs):
        err, msg = self.os.run("docker ps -q")
        if err:
            return False
        else:
            if msg:
                err, msg = self.os.run("docker stop {0}".format(" ".join(self.os.string_clean(msg))))
                if err:
                    return False

        err, msg = self.os.run("docker ps -qa")
        if err:
            return False
        else:
            err, msg = self.os.run("docker rm {0}".format(" ".join(self.os.string_clean(msg))))
            if err:
                return False
            else:
                return True

    def clear_images(self, *args, **kwargs):
        err, msg = self.os.run("docker images -qa")
        if err:
            return False
        else:
            err, msg = self.os.run("docker rmi -f {0}".format(" ".join(self.os.string_clean(msg))))
            if err:
                return False
            else:
                return True

    def container_exist(self, container, running=False, *args, **kwargs):
        err, msg = self.os.run("docker ps {0}".format("-a" if not running else ""))
        if err:
            return False
        else:
            if container in "".join(msg):
                return True
            else:
                return False

    def image_exist(self, image, *args, **kwargs):
        err, msg = self.os.run("docker images")
        if err:
            return False
        else:
            if image in "".join(msg):
                return True
            else:
                return False

    def login(self, name, pwd, host="", *args, **kwargs):
        err, msg = self.os.run("docker login --username={0} --password={1} {2}".format(name, pwd, host))
        return not err