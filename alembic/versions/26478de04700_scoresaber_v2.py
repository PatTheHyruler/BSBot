"""ScoreSaber v2

Revision ID: 26478de04700
Revises: a52babf8eefa
Create Date: 2022-04-07 13:34:57.656769

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
from src.kiyomi import EMapTagList
from src.kiyomi.database.types.string_list import StringList

revision = '26478de04700'
down_revision = 'a52babf8eefa'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('leaderboard',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('song_hash', sa.String(length=128), nullable=True),
    sa.Column('song_name', sa.String(length=128), nullable=True),
    sa.Column('song_sub_name', sa.String(length=128), nullable=True),
    sa.Column('song_author_name', sa.String(length=128), nullable=True),
    sa.Column('level_author_name', sa.String(length=128), nullable=True),
    sa.Column('max_score', sa.Integer(), nullable=True),
    sa.Column('ranked', sa.Boolean(), nullable=True),
    sa.Column('qualified', sa.Boolean(), nullable=True),
    sa.Column('loved', sa.Boolean(), nullable=True),
    sa.Column('stars', sa.Float(), nullable=True),
    sa.Column('positive_modifiers', sa.Boolean(), nullable=True),
    sa.Column('plays', sa.Integer(), nullable=True),
    sa.Column('daily_plays', sa.Integer(), nullable=True),
    sa.Column('cover_image', sa.String(length=256), nullable=True),
    sa.Column('max_pp', sa.Float(), nullable=True),
    sa.Column('created_date', sa.DateTime(), nullable=True),
    sa.Column('ranked_date', sa.DateTime(), nullable=True),
    sa.Column('qualified_date', sa.DateTime(), nullable=True),
    sa.Column('loved_date', sa.DateTime(), nullable=True),
    sa.Column('difficulty_raw', sa.String(length=64), nullable=True),
    sa.Column('game_mode', sa.Enum('STANDARD', 'ONE_SABER', 'NO_ARROWS', 'DEGREE_90', 'DEGREE_360', 'LIGHTSHOW', 'LAWLESS', 'UNKNOWN', name='gamemode'), nullable=True),
    sa.Column('difficulty', sa.Enum('EASY', 'NORMAL', 'HARD', 'EXPERT', 'EXPERT_PLUS', 'UNKNOWN', name='beatmapdifficulty'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('echo_emoji',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('emoji_id', sa.BigInteger(), nullable=True),
    sa.Column('guild_id', sa.BigInteger(), nullable=True),
    sa.ForeignKeyConstraint(['emoji_id'], ['emoji.id'], ),
    sa.ForeignKeyConstraint(['guild_id'], ['guild.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('message',
    sa.Column('id', sa.BigInteger(), autoincrement=False, nullable=False),
    sa.Column('guild_id', sa.BigInteger(), nullable=True),
    sa.Column('channel_id', sa.BigInteger(), nullable=True),
    sa.ForeignKeyConstraint(['channel_id'], ['channel.id'], ),
    sa.ForeignKeyConstraint(['guild_id'], ['guild.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('message_view',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('view_name', sa.String(length=128), nullable=True),
    sa.Column('view_parameters', StringList(), nullable=True),
    sa.Column('message_id', sa.BigInteger(), nullable=True),
    sa.ForeignKeyConstraint(['message_id'], ['message.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('beatmap', sa.Column('tags', EMapTagList(), nullable=True))
    op.add_column('beatmap_version_difficulty', sa.Column('stars', sa.Float(), nullable=True))
    op.drop_constraint('guild_player_ibfk_3', 'guild_player', type_='foreignkey')
    op.create_foreign_key(None, 'guild_player', 'player', ['player_id'], ['id'], ondelete='CASCADE')
    op.add_column('player', sa.Column('name', sa.String(length=128), nullable=True))
    op.add_column('player', sa.Column('score_stats_total_score', sa.BigInteger(), nullable=True))
    op.add_column('player', sa.Column('score_stats_total_ranked_score', sa.BigInteger(), nullable=True))
    op.add_column('player', sa.Column('score_stats_average_ranked_accuracy', sa.Float(), nullable=True))
    op.add_column('player', sa.Column('score_stats_total_play_count', sa.Integer(), nullable=True))
    op.add_column('player', sa.Column('score_stats_ranked_play_count', sa.Integer(), nullable=True))
    op.add_column('player', sa.Column('score_stats_replays_watched', sa.Integer(), nullable=True))
    op.drop_column('player', 'player_name')
    op.drop_column('player', 'badges')
    op.add_column('score', sa.Column('base_score', sa.Integer(), nullable=True))
    op.add_column('score', sa.Column('modified_score', sa.Integer(), nullable=True))
    op.add_column('score', sa.Column('modifiers', sa.String(length=128), nullable=True))
    op.add_column('score', sa.Column('multiplier', sa.String(length=128), nullable=True))
    op.add_column('score', sa.Column('bad_cuts', sa.Integer(), nullable=True))
    op.add_column('score', sa.Column('missed_notes', sa.Integer(), nullable=True))
    op.add_column('score', sa.Column('max_combo', sa.Integer(), nullable=True))
    op.add_column('score', sa.Column('full_combo', sa.Boolean(), nullable=True))
    op.add_column('score', sa.Column('hmd', sa.Integer(), nullable=True))
    op.add_column('score', sa.Column('has_replay', sa.Boolean(), nullable=True))
    op.drop_column('score', 'leaderboard_id')
    op.add_column('score', sa.Column('leaderboard_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'score', 'leaderboard', ['leaderboard_id'], ['id'], ondelete='CASCADE')
    op.drop_column('score', 'mods')
    op.drop_column('score', 'unmodified_score')
    op.drop_column('score', 'score')
    op.drop_column('score', 'difficulty')
    op.drop_column('score', 'song_hash')
    op.drop_column('score', 'max_score')
    op.drop_column('score', 'song_name')
    op.drop_column('score', 'characteristic')
    op.drop_column('score', 'song_sub_name')
    op.drop_column('score', 'level_author_name')
    op.drop_column('score', 'song_author_name')
    op.alter_column('setting', 'setting_type',
               existing_type=mysql.ENUM('INT', 'STRING', 'BOOLEAN', 'CHANNEL'),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('setting', 'setting_type',
               existing_type=mysql.ENUM('INT', 'STRING', 'BOOLEAN', 'CHANNEL'),
               nullable=False)
    op.add_column('score', sa.Column('song_author_name', mysql.VARCHAR(length=128), nullable=True))
    op.add_column('score', sa.Column('level_author_name', mysql.VARCHAR(length=128), nullable=True))
    op.add_column('score', sa.Column('song_sub_name', mysql.VARCHAR(length=128), nullable=True))
    op.add_column('score', sa.Column('characteristic', mysql.ENUM('STANDARD', 'ONE_SABER', 'NO_ARROWS', 'DEGREE_90', 'DEGREE_360', 'LIGHTSHOW', 'LAWLESS', 'UNKNOWN'), nullable=True))
    op.add_column('score', sa.Column('song_name', mysql.VARCHAR(length=128), nullable=True))
    op.add_column('score', sa.Column('max_score', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.add_column('score', sa.Column('song_hash', mysql.VARCHAR(length=128), nullable=True))
    op.add_column('score', sa.Column('difficulty', mysql.ENUM('EASY', 'NORMAL', 'HARD', 'EXPERT', 'EXPERT_PLUS', 'UNKNOWN'), nullable=True))
    op.add_column('score', sa.Column('score', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.add_column('score', sa.Column('unmodified_score', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.add_column('score', sa.Column('mods', mysql.VARCHAR(length=128), nullable=True))
    op.drop_constraint(None, 'score', type_='foreignkey')
    op.drop_column('score', 'has_replay')
    op.drop_column('score', 'hmd')
    op.drop_column('score', 'full_combo')
    op.drop_column('score', 'max_combo')
    op.drop_column('score', 'missed_notes')
    op.drop_column('score', 'bad_cuts')
    op.drop_column('score', 'multiplier')
    op.drop_column('score', 'modifiers')
    op.drop_column('score', 'modified_score')
    op.drop_column('score', 'base_score')
    op.add_column('player', sa.Column('badges', mysql.LONGTEXT(charset='utf8mb4', collation='utf8mb4_bin'), nullable=True))
    op.add_column('player', sa.Column('player_name', mysql.VARCHAR(length=128), nullable=True))
    op.drop_column('player', 'score_stats_replays_watched')
    op.drop_column('player', 'score_stats_ranked_play_count')
    op.drop_column('player', 'score_stats_total_play_count')
    op.drop_column('player', 'score_stats_average_ranked_accuracy')
    op.drop_column('player', 'score_stats_total_ranked_score')
    op.drop_column('player', 'score_stats_total_score')
    op.drop_column('player', 'name')
    op.drop_constraint(None, 'guild_player', type_='foreignkey')
    op.create_foreign_key('guild_player_ibfk_3', 'guild_player', 'player', ['player_id'], ['id'])
    op.drop_column('beatmap_version_difficulty', 'stars')
    op.drop_column('beatmap', 'tags')
    op.drop_table('message_view')
    op.drop_table('message')
    op.drop_table('echo_emoji')
    op.drop_table('leaderboard')
    # ### end Alembic commands ###
