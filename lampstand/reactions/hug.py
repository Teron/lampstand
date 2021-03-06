import re
import time
import random
import sys
import lampstand.reactions.base

import logging


def __init__():
    pass


class Reaction(lampstand.reactions.base.Reaction):
    __name = 'Hug'

    cooldown_number = 5
    cooldown_time = 120
    uses = []

    def __init__(self, connection):
        self.logger = logging.getLogger(self.__name)

        self.default = "chocolate"

        self.banned = {}  # {'entimix': 'rickroller'}

        self.channelMatch = re.compile(
            '.*hugs %s' %
            connection.nickname,
            re.IGNORECASE)
        self.privateMatch = re.compile('give me (.*)\.?', re.IGNORECASE)

        self.dbconnection = connection.dbconnection

    def channelAction(self, connection, user, channel, message):

        if self.overUsed():
            self.logger.info("[HUG REACTION] OVERUSED %s" % user)
            connection.message(
                channel,
                "%s: I am not a vending machine :(" %
                user)
            return

        if (user.lower() in self.banned):
            self.logger.info("[HUG REACTION] BANNED %s" % user)
            insult = shakeinsult.shakeinsult(1)
            connection.message(
                channel,
                "%s the %s, %s" %
                (user,
                 self.banned[
                     user.lower()],
                    insult))
            return

        self.updateOveruse()

        self.logger.info("[HUG REACTION] GET %s" % user)
        connection.describe(
            channel,
            self.hug(user).decode("utf-8").encode("utf-8"))
        return True

    def privateAction(self, connection, user, channel, message):

        item = self.privateMatch.findall(message)

        self.logger.info("[HUG REACTION] SET %s %s" % (user, item[0]))
        connection.message(user, self.set(user, item[0]))

    def set(self, username, item):
        cursor = self.dbconnection.cursor()
        cursor.execute(
            'delete FROM hugReaction where username LIKE %s',
            (username.lower(),
             ))
        cursor.execute(
            'replace into hugReaction (username, item) values (%s, %s)',
            (username.lower(),
             item))
        self.dbconnection.commit()

        self.logger.info("Set %s hug reaction to %s" % (username, item))
        return "When you hug me, I'll give you '%s'" % item

    def hug(self, username):
        self.logger.info("Hug %s" % username)
        cursor = self.dbconnection.cursor()
        cursor.execute(
            'SELECT * FROM hugReaction where username LIKE %s',
            (username.lower(),
             ))
        result = cursor.fetchone()

        if result is not None:
            self.logger.info("I have a replacement for %s: %s" %
                             (username, result[1]))
            return "gives %s %s " % (username, result[1])

        else:
            self.logger.info("I have no replacement for %s" % username)
            return "gives %s %s " % (username, self.default)
