import commands
import unittest
from unittest import mock
from click.testing import CliRunner

class TestIgnoreCommand(unittest.TestCase):

    @mock.patch("commands.os")
    def test_repo_without_gitignore(self, os_mock):
        os_mock.path.exists.return_value = False
        gitignore_files = commands.get_gitignore_files("git path")
        self.assertEqual(len(gitignore_files), 0)
        self.assertIsInstance(gitignore_files, list)

    @mock.patch("commands.os")
    @mock.patch("builtins.open", new_callable = mock.mock_open, read_data="\na1\n  \n\na2\na3\n")
    def test_repo_with_gitignore(self, open_mock, os_mock):
        os_mock.path.exists.return_value = True

        gitignore_files = commands.get_gitignore_files("git path")
        self.assertEqual(len(gitignore_files), 3)

    @mock.patch("commands.os")
    def test_get_dir_files(self, os_mock):
        files = ["archivo1", "archivo2", "archivo3"]
        output = {k:{"file_name": f"inside path/{k}", "is_folder": False} for k in files}

        os_mock.listdir.return_value = files
        os_mock.path.isdir.return_value = False

        dir_files = commands.get_files("git path/inside path", "git path")

        self.assertDictEqual(dir_files, output)

    @mock.patch("commands.os")
    def test_get_dir_folders(self, os_mock):
        files = ["folder1", "folder2", "folder3"]
        output = {f"{k}/":{"file_name": f"inside path/{k}/", "is_folder": True} for k in files}

        os_mock.listdir.return_value = files
        os_mock.path.isdir.return_value = True

        dir_files = commands.get_files("git path/inside path", "git path")

        self.assertDictEqual(dir_files, output)

    @mock.patch("commands.os")
    def test_get_dir_files_top(self, os_mock):
        files = ["archivo1", "archivo2", "archivo3"]
        output = {k:{"file_name": k, "is_folder": False} for k in files}

        os_mock.listdir.return_value = files
        os_mock.path.isdir.return_value = False

        dir_files = commands.get_files("git path", "git path")

        self.assertDictEqual(dir_files, output)

    def test_choices(self):
        dir_files = {
            "a1":{
                "file_name": "inside path/a1",
                "is_folder": False
            },
            "a2":{
                "file_name": "inside path/a2",
                "is_folder": False
            },
            "a3":{
                "file_name": "inside path/a3",
                "is_folder": False
            },
            "f1/":{
                "file_name": "inside path/f1/",
                "is_folder": True
            },
            "f2/":{
                "file_name": "inside path/f2/",
                "is_folder": True
            },
            "f3/":{
                "file_name": "inside path/f3/",
                "is_folder": True
            }
        }

        gitignore_files = ["a1", "inside path/a2","inside path/inside/f1/", "inside path/f2/"]

        expected_output = [
            {"name": "a1"},
            {"name": "a2", "checked": True},
            {"name": "a3"},
            {"name": "f1/"},
            {"name": "f2/", "checked": True},
            {"name": "f3/"},
        ]

        choices = commands.create_choices(dir_files, gitignore_files)
        self.assertListEqual(choices, expected_output)

        for key in ["a2", "f2/"]:
            self.assertTrue(dir_files[key]["is_ignored"])

        for key in ["a1", "f1/", "a3", "f3/"]:
            self.assertFalse(dir_files[key]["is_ignored"])
    
    @mock.patch("builtins.open")
    def test_update_gitignore_add_files(self, open_mock):
        dir_files = {
            "a1":{
                "file_name": "inside path/a1",
                "is_folder": False,
                "is_ignored": False
            },
            "a2":{
                "file_name": "inside path/a2",
                "is_folder": False,
                "is_ignored": True
            },
            "a3":{
                "file_name": "inside path/a3",
                "is_folder": False,
                "is_ignored": False
            },
            "f1/":{
                "file_name": "inside path/f1/",
                "is_folder": True,
                "is_ignored": False
            },
            "f2/":{
                "file_name": "inside path/f2/",
                "is_folder": True,
                "is_ignored": True
            },
            "f3/":{
                "file_name": "inside path/f3/",
                "is_folder": True,
                "is_ignored": False
            }
        }
        gitignore_files = ["a1", "inside path/a2","inside path/inside/f1/", "inside path/f2/"]
        answers = ["a1", "a2", "f2/", "f3/"]

        ignored_files = gitignore_files + ["a1", "f3/"]
        ignored_files = "\n".join(ignored_files)

        open_mock = mock.mock_open()

        new_files = commands.update_gitignore(answers, dir_files, gitignore_files, "git path")
        
        self.assertListEqual(new_files, ["a1", "f3/"])

        open_mock.assert_called_once_with('git path/.gitignore', 'w')
        handle = open_mock()
        handle.write.assert_called_once_with(ignored_files)

        

if __name__ == '__main__':
    unittest.main()