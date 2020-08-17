import unittest
from unittest import mock
import commands
from click.testing import CliRunner

class TestInitCommand(unittest.TestCase):

    @mock.patch('commands.git')
    def test_is_initialized_true(self, mock_git):
        is_initialized = commands.is_initialized_repo()
        self.assertTrue(is_initialized)

    @mock.patch('commands.git')
    def test_is_initialized_false(self, mock_git):
        mock_git.Repo.side_effect = Exception()
        is_initialized = commands.is_initialized_repo()
        self.assertFalse(is_initialized)

    @mock.patch('commands.Github')
    @mock.patch('commands.init_local_repo')
    @mock.patch('commands.is_initialized_repo')
    def test_init_github_exception(
        self,
        mock_is_initialized_repo, 
        mock_init_local_repo, 
        mock_Github
        ):
        mock_is_initialized_repo.return_value = False
        mock_Github.side_effect = Exception()
        runner = CliRunner()
        result = runner.invoke(commands.init, 
        ['-u', 'user', '-p', 'passwrod', '-r', 'repo_name'])
        self.assertFalse(mock_init_local_repo.called)

    @mock.patch('commands.Github')
    @mock.patch('commands.init_local_repo')
    @mock.patch('commands.is_initialized_repo')
    def test_init_already_initialized(
        self,
        mock_is_initialized_repo, 
        mock_init_local_repo, 
        mock_Github
        ):
        mock_is_initialized_repo.return_value = True
        runner = CliRunner()
        result = runner.invoke(commands.init, 
        ['-u', 'user', '-p', 'passwrod', '-r', 'repo_name'])
        self.assertFalse(mock_Github.called)
        self.assertFalse(mock_init_local_repo.called)

    @mock.patch('commands.Github')
    @mock.patch('commands.init_local_repo')
    @mock.patch('commands.is_initialized_repo')
    def test_init_local_only(
        self,
        mock_is_initialized_repo, 
        mock_init_local_repo, 
        mock_Github
        ):
        mock_is_initialized_repo.return_value = False
        runner = CliRunner()
        result = runner.invoke(commands.init, 
        ['-l'])
        self.assertFalse(mock_Github.called)
        self.assertTrue(mock_init_local_repo.called)
