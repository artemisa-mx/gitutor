import unittest
from unittest import mock
import commands
from click.testing import CliRunner

class TestSaveCommand(unittest.TestCase):

    @mock.patch('commands.repo.git.commit')
    @mock.patch('commands.get_conflict_files')
    @mock.patch('commands.repo.remotes.origin.exists')
    @mock.patch('commands.repo.git.pull')
    @mock.patch('commands.conflicts_from_merge')
    @mock.patch('commands.repo.git.push')
    def test_save_commit_exception(
        self,
        mock_get_conflict_files, 
        mock_commit,
        mock_exists,
        mock_pull,
        mock_conflicts_from_merge,
        mock_push
        ):
        mock_get_conflict_files.return_value = False
        mock_commit.side_effect = Exception()
        mock_exists.return_value = True
        mock_pull.return_value = True
        runner = CliRunner()
        result = runner.invoke(commands.save, 
        ['-m', 'message'])
        self.assertTrue(mock_push.called)

    @mock.patch('commands.repo.git.commit')
    @mock.patch('commands.get_conflict_files')
    @mock.patch('commands.repo.remotes.origin.exists')
    @mock.patch('commands.repo.git.pull')
    @mock.patch('commands.conflicts_from_merge')
    @mock.patch('commands.repo.git.push')
    @mock.patch('commands.click.echo')
    def test_save_conflicted_files(
        self,
        mock_get_conflict_files, 
        mock_commit,
        mock_exists,
        mock_pull,
        mock_conflicts_from_merge,
        mock_echo
        ):
        mock_get_conflict_files.return_value = True
        mock_commit.side_effect = Exception()
        mock_exists.return_value = True
        mock_pull.return_value = True
        runner = CliRunner()
        result = runner.invoke(commands.save, 
        ['-m', 'message'])
        mock_echo.assert_called_with('Please fix the following conflicts then use "gt save" again')