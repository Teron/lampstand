from lampstand import bible
from lampstand.tools import splitAt
import re
import time
import random
import sys
import lampstand.reactions.base


def __init__():
    pass


class Reaction(lampstand.reactions.base.Reaction):
    __name = 'Bible'

    cooldown_number = 3
    cooldown_time = 120
    uses = []
    #List of unique book names in ESV bible ignoring preceding numbers.
    _bibleBooks = ["Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy",
                   "Joshua", "Judges", "Ruth", "Samuel", "Kings", "Chronicles",
                   "Ezra", "Nehemiah", "Esther", "Job", "Psalms", "Proverbs",
                   "Ecclesiastes", "Song of Solomon", "Isaiah", "Jeremiah",
                   "Lamentations", "Ezekiel", "Daniel", "Hosea", "Joel", "Amos",
                   "Obadiah", "Jonah", "Micah", "Nahum", "Habakkuk", "Zephaniah",
                   "Haggai", "Zechariah", "Malachi", "Matthew", "Mark", "Luke",
                   "John", "Acts", "Romans", "Corinthians", "Galatians",
                   "Ephesians", "Philippians", "Colossians", "Thessalonians",
                   "Timothy", "Titus", "Philemon", "Hebrews", "James", "Peter",
                   "Jude", "Revelation"]
    def bookPartRegex():
        #Generate regex that matches 3 or more characters of any of the books
        #starting from the front
        #i.e will match "Joshua" "Joshu" "Josh" "Jos"
        #As esvbible does not return matches for 1 and 2 length strings
        pass
    def __init__(self, connection):
        self.channelMatch = re.compile(
            '%s. %s (\d+\:\S+)' %
            (connection.nickname,bookPartRegex()),
            re.IGNORECASE)
        self.privateMatch = re.compile('%s (\d+\:\S+)' % bookPartRegex())

    def channelAction(self, connection, user, channel, message):
        matches = self.channelMatch.findall(message)

        if self.overUsed():
            connection.message(
                user,
                "Enough with the religion for now. (Overuse triggered)")
            return

        print "[Bible] %s" % matches

        bibleConnection = bible.ESVSession()
        result = bibleConnection.doPassageQuery(
            '%s %s' %
            (matches[0][0], matches[0][1]))

        result = ' '.join(result.split('\n'))

        self.updateOveruse()

        if len(result) > 880 * 2:

            whereToSplit = splitAt(result, 860)
            result = "%s [Cut for length]" % result[0:whereToSplit]

        if len(result) > 440:
            whereToSplit = splitAt(result, 440)
            stringOne = result[0:whereToSplit]
            stringTwo = result[whereToSplit:]

            connection.message(channel, "%s... " % stringOne)
            connection.message(channel, "... %s [ESV]" % stringTwo)
        else:
            connection.message(channel, "%s [ESV]" % result)

        return True

    def privateAction(self, connection, user, channel, message):
        matches = self.privateMatch.findall(message)

        print "[Bible] %s" % matches

        bibleConnection = bible.ESVSession()
        result = bibleConnection.doPassageQuery(
            '%s %s' %
            (matches[0][0], matches[0][1]))

        result = ' '.join(result.split('\n'))

        if len(result) > 880 * 2:

            whereToSplit = splitAt(result, 860)
            result = "%s [Cut for length]" % result[0:whereToSplit]

        if len(result) > 440:
            whereToSplit = splitAt(result, 440)
            stringOne = result[0:whereToSplit]
            stringTwo = result[whereToSplit:]

            connection.message(user, "%s... " % stringOne)
            connection.message(user, "... %s [ESV]" % stringTwo)
        else:
            connection.message(user, "%s [ESV]" % result)

        return True
