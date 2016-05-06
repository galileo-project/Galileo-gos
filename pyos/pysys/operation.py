from subprocess import Popen, PIPE
import shlex
import re
import os
from pyos.utils.string import decode as str_decode
from pyos.utils.string import is_str

class SysOperation(object):
    _RE_CD = re.compile(r"cd\s([\w\d_\/\s\~\.]+)")

    @classmethod
    def mkdir(cls, paths, force=False, *args, **kwargs):
        if not isinstance(paths, list):
            paths = [paths]

        paths = cls.rel2abs(paths)

        for path in paths:
            if cls.exist(path):
                if force:
                    cls.rm(path)
                else:
                    paths.remove(path)

        err , msg = cls.__exec("mkdir -p %s" % " ".join(paths), *args, **kwargs)

        return not err

    @classmethod
    def rm(cls, paths, *args, **kwargs):
        if not isinstance(paths, list):
            paths = [paths]

        paths = cls.rel2abs(paths)

        if paths:
            err, msg = cls.__exec("rm -rf %s" % " ".join(paths), *args, **kwargs)
            return not err
        else:
            return True

    @classmethod
    def ls(cls, path=None, hidden=False, *args, **kwargs):
        cmd = "ls %s" % cls.rel2abs(path)
        if hidden:
            cmd = "%s %s" % (cmd, "-a")
        err, msg = cls.__exec(cmd)

        if err:
            return []
        else:
            return cls.string_clean(msg)

    @classmethod
    def cp(cls, origin, target, *args, **kwargs):
        if not isinstance(origin, list):
            origin = [origin]

        origin = cls.rel2abs(origin)
        target = cls.rel2abs(target)

        err, msg = cls.__exec("cp -rf %s %s" % (" ".join(origin), target))
        return not err

    @classmethod
    def chmod(cls, mod, path, *args, **kwargs):
        if not isinstance(path, list):
            path = [path]

        path = cls.rel2abs(path)

        err, msg = cls.__exec("chmod %d %s" % (mod, " ".join(path)), *args, **kwargs)
        return not err

    @classmethod
    def run(cls, cmd, path = None, paras=None, *args, **kwargs):
        if path:
            path = cls.rel2abs(path)
        return cls.__exec(cmd, cwd = path, paras=paras, *args, **kwargs)


    @classmethod
    def cat(cls, paths, *args, **kwargs):
        if not isinstance(paths, list):
            paths = [paths]

        paths = cls.rel2abs(paths)

        err, msg = cls.__exec("cat %s" % " ".join(paths))
        if err:
            return ""
        else:
            return cls.string_clean(msg)

    @classmethod
    def pwd(cls, *args, **kwargs):
        path = os.path.curdir
        return cls.rel2abs(path)

    @classmethod
    def read(cls, path, *args, **kwargs):
        path = cls.rel2abs(path)
        with open(path, "r") as stream:
            lines = [str_decode(line) for line in stream.readlines()]

        return lines

    @classmethod
    def find(cls, path, name = None, depth = 1, *args, **kwargs):
        if not name:
            target_path = os.path.dirname(path)
        else:
            target_path = path
        target_name = name or os.path.basename(path)

        err, msg = cls.__exec("find %s -maxdepth %d -name %s" % (cls.rel2abs(target_path), depth, target_name), *args, **kwargs)

        if err:
            return []
        return cls.string_clean(msg)

    @classmethod
    def distr(cls, *args, **kwargs):
        paths = cls.find("/etc/*-release")
        ret = cls.cat(paths)
        re_distri = re.compile(r'PRETTY_NAME=\"(.*?)\"')
        return re_distri.findall(ret)[0]

    @classmethod
    def append(cls, path, contents, *args, **kwargs):
        path = cls.rel2abs(path)
        content = contents.join("\n")
        err, msg = cls.__exec("sed -i '$a %s' %s" % (content, path), *args, **kwargs)
        return not err

    @classmethod
    def exist(cls, path, *args, **kwargs):
        path = cls.rel2abs(path)
        return os.path.exists(path)

    @classmethod
    def rel2abs(cls, paths = None, *args, **kwargs):
        rets = []
        para_type = list
        if not isinstance(paths, list):
            paths = [paths]
            para_type = str

        for path in paths:
            if path is not None:
                if "~" in path:
                    if cls.get_user() == "root":
                        path = path.replace("~", "/root")
                    else:
                        path = path.replace("~", "/home/%s" % cls.get_user())
                ret = os.path.abspath(path)
            else:
                ret = os.curdir

            rets.append(ret)

        if para_type is str:
            return rets[0]
        else:
            return rets

    @classmethod
    def touch(cls, path, content="", *args, **kwargs):
        with open(path, "w+") as stream:
            stream.write(content)
        return True

    @property
    def user(self):
        return self.get_user()

    @staticmethod
    def get_user():
        return os.getenv("USER")

    @classmethod
    def __exec(cls, cmd, cwd = None, paras=None, *args, **kwargs):
        if "&&" in cmd:
            cmds = cmd.split("&&")
            err  = False
            msg  = None
            path = None

            for cmd in cmds:
                if not path:
                    path = cls.__cd_to_path(cwd)
                    if path: continue
                err, msg = cls.__exec(cmd, cwd=path or cwd, *args, **kwargs)
                if err:
                    return err, msg
                else:
                    continue
            return err, msg

        cmd_args = shlex.split(cmd)
        p = Popen(cmd_args, cwd=cwd, stderr=PIPE, stdout=PIPE, stdin=PIPE, shell=False)
        if paras:
            if not isinstance(paras, list):
                paras = [paras]

            for para in paras:
                p.stdin.write("%s\n" % para)
                # try:
                #     p.stdin.write("%s\n" % para)
                # except:
                #     pass
            p.stdin.close()

        return cls.__parser(p, *args, **kwargs)

    @classmethod
    def string_clean(cls, strings):
        if isinstance(strings, list):
            ret = []
            for string in strings:
                ret.append(cls.string_clean(string))
            return ret
        else:
            if is_str(strings):
                strings = strings.replace("\n", "")
                strings = strings.replace("\t", "")
            return strings

    @classmethod
    def __cd_to_path(cls, cmd):
        ret = cls._RE_CD.findall(cmd)
        if ret:
            return cls.rel2abs(ret[0])
        else:
            return None

    @staticmethod
    def __parser(process, *args, **kwargs):
        process.wait()
        code = process.poll()

        out_strs = [str_decode(line) for line in process.stdout.readlines()]
        err_strs = [str_decode(line) for line in process.stderr.readlines()]

        if code != 0:
            return True, err_strs
        else:
            return False, out_strs
