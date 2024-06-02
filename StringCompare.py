class StringCompare:
    def __init__(self, s1, s2):
        self.s1 = s1
        self.s2 = s2

    def compare(self):
        """
        Compare two strings
        :return: bool, True if the strings are equal, False otherwise
        """
        return self.s1 == self.s2

    def substring(self):
        """
        Is s2 a substring of s1
        :return: bool, True if s2 is a substring of s1, False otherwise
        """
        is_substring = self.s2 in self.s1
        print(f"{self.s2} is a substring of {self.s1}: {is_substring}")
        return is_substring
