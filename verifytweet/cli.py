# Verify Tweet verifies tweets of a public user
# from tweet screenshots: real or generated from
# tweet generators.
# Copyright (C) 2019 Preetham Kamidi

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import click

from .services import controller
from .config.settings import app_config
from .util.logging import logger
from .util.result import ResultStatus


@click.command()
@click.option("--filepath",
              "-f",
              required=True,
              help="The filepath for the tweet screenshot image",
              type=click.Path(exists=True,
                              dir_okay=False,
                              resolve_path=True,
                              readable=True))
def run_as_command(filepath):
    """Verifies tweet from given image.

    Verifies tweet from image given via file path
    using a combination of image processing, text processing
    as well as a search service.

    Args:
        filepath: The filepath for the tweet screenshot image.
    
    Returns:
        Prints validity of a tweet

    """

    try:
        verify_controller = controller.NonAPIApproach()
        tweet_obj, controller_status = verify_controller.exec(filepath)
        if controller_status == ResultStatus.MODULE_FAILURE:
            print(f"Something went wrong, Please try again!")
        elif controller_status == ResultStatus.NO_RESULT:
            print(f"Fake Tweet!")
        else:
            print(f"\nVerified Tweet!")
            print(
                f"**** Username: {tweet_obj.username} ****\n**** Tweet: {tweet_obj.tweet} ****\n**** Likes: {tweet_obj.likes_count} ****\n**** Retweets: {tweet_obj.retweets_count} ****\n**** Link: {tweet_obj.link} ****"
            )
    except Exception as e:
        logger.exception(e)
