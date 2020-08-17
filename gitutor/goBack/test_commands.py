import unittest
from unittest import mock
import commands
from click.testing import CliRunner
from git import Repo

class TestGoBackCommand(unittest.TestCase):

    # @mock.patch('commands.git')
    # def test_is_initialized_true(self, mock_git):
    #     is_initialized = commands.is_initialized_repo()
    #     self.assertTrue(is_initialized)

    @mock.patch('commands.revert_hash_sequence')
    @mock.patch('commands.hash_sequence_to_target')
    def test_revert_to_target_empty_hash_sequence(
        self,
        mock_hash_seq_to_target,
        mock_revert_hash_seq
    ):
        repo = mock.Mock(spec=Repo)
        mock_hash_seq_to_target.side_effect = [
            [1],
            []
        ]
        number_of_reverts = commands.revert_to_target(repo, 1, [])
        self.assertFalse(mock_revert_hash_seq.called)
        self.assertFalse(repo.git.called)
        self.assertTrue(mock_hash_seq_to_target.called)
        self.assertEqual(number_of_reverts, 0)

    @mock.patch('commands.revert_hash_sequence')
    @mock.patch('commands.hash_sequence_to_target')
    def test_revert_to_target_succesfull(
        self,
        mock_hash_seq_to_target,
        mock_revert_hash_seq
    ):
        repo = mock.Mock(spec=Repo)
        mock_hash_seq_to_target.side_effect = [
            [1, 2, 3],
            [1, 2, 3]
        ]
        number_of_reverts = commands.revert_to_target(repo, 1, [])
        self.assertTrue(mock_revert_hash_seq.called)
        self.assertFalse(repo.git.called)
        self.assertTrue(mock_hash_seq_to_target.called)
        self.assertEqual(number_of_reverts, 3)

    @mock.patch('commands.revert_hash_sequence')
    @mock.patch('commands.hash_sequence_to_target')
    def test_revert_to_target_fails(
        self,
        mock_hash_seq_to_target,
        mock_revert_hash_seq
    ):
        repo = mock.Mock(spec=Repo)
        mock_hash_seq_to_target.side_effect = [
            [1, 2, 3],
            [1, 2, 3]
        ]
        mock_revert_hash_seq.side_effect = Exception
        number_of_reverts = commands.revert_to_target(repo, 1, [])
        self.assertTrue(mock_revert_hash_seq.called)
        self.assertTrue(mock_hash_seq_to_target.called)
        repo.git.reset.assert_called_with('--hard', 1)
        self.assertEqual(number_of_reverts, 0)

    