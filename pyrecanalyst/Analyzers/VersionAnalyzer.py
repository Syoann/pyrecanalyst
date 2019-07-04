from pyrecanalyst.Model.Version import Version
from pyrecanalyst.Analyzers.Analyzer import Analyzer


class VersionAnalyzer(Analyzer):
    """Determine the game version that created the recorded game file."""
    # Trial game version IDs.
    trial_versions = [
        Version.VERSION_AOKTRIAL,
        Version.VERSION_AOCTRIAL,
    ]

    # UserPatch game version IDs.
    userpatch_versions = [
        Version.VERSION_USERPATCH11,
        Version.VERSION_USERPATCH12,
        Version.VERSION_USERPATCH13,
        Version.VERSION_USERPATCH14,
        Version.VERSION_USERPATCH15,
        Version.VERSION_AOFE21,
    ]

    # Age of Kings game version IDs.
    aok_versions = [
        Version.VERSION_AOK,
        Version.VERSION_AOKTRIAL,
        Version.VERSION_AOK20,
        Version.VERSION_AOK20A,
    ]

    # Age of Conquerors expansion game version IDs.
    aoc_versions = [
        Version.VERSION_AOC,
        Version.VERSION_AOCTRIAL,
        Version.VERSION_AOC10,
        Version.VERSION_AOC10C,
    ]

    # HD Edition game version IDs.
    hd_versions = [
        Version.VERSION_HD,
        Version.VERSION_HD43,
        Version.VERSION_HD46,
        # Currently unused: HD 4.6 and 4.7 use the same file format, so we can't
        # easily detect which one it is.
        Version.VERSION_HD47,
        Version.VERSION_HD48,
        Version.VERSION_HD50
    ]

    def run(self):
        """Read recorded game version metadata."""
        version_string = self.read_header_raw(8).rstrip(b' \x00').decode()
        sub_version = round(self.read_header('<f', 4), 2)

        version = self.get_version(version_string, sub_version)

        analysis = Version(self.rec, version_string, sub_version)
        analysis.version = version

        analysis.is_trial = version in VersionAnalyzer.trial_versions
        analysis.is_aok = version in VersionAnalyzer.aok_versions
        analysis.is_user_patch = version in VersionAnalyzer.userpatch_versions
        analysis.is_user_patch15 = (version == Version.VERSION_USERPATCH15)
        analysis.is_hd_edition = version in VersionAnalyzer.hd_versions
        analysis.is_hd_patch4 = analysis.is_hd_edition and sub_version >= 12.00
        analysis.is_aoc = analysis.is_user_patch or analysis.is_hd_edition or version in VersionAnalyzer.aoc_versions

        analysis.is_mgl = analysis.is_aok
        analysis.is_mgx = analysis.is_aoc
        analysis.is_mgz = analysis.is_user_patch
        # FIXME Not sure if this is the correct cutoff point.
        #
        # test/recs/versions/mgx2_simple.mgx2
        #    has subVersion == 12.31
        # test/recs/versions/MP Replay v4.3 @2015.09.11 221142 (2).msx
        #    has subVersion == 12.34
        # So it's somewhere between those two.
        analysis.is_msx = sub_version >= 12.32
        analysis.is_aoe2_record = sub_version >= 12.36

        return analysis

    def get_version(self, version, sub_version):
        """Get the version ID from a version string and sub-version number."""
        if version == 'TRL 9.3':
            if self.is_mgx:
                return Version.VERSION_AOCTRIAL
            else:
                return Version.VERSION_AOKTRIAL
        elif version == 'VER 9.3':
            return Version.VERSION_AOK
        elif version == 'VER 9.4':
            if sub_version >= 12.50:
                return Version.VERSION_HD50
            if sub_version >= 12.49:
                return Version.VERSION_HD48
            if sub_version >= 12.36:
                # Patch versions 4.6 and 4.7.
                return Version.VERSION_HD46
            if sub_version >= 12.34:
                # Probably versions 4.3 through 4.5?
                return Version.VERSION_HD43
            if sub_version > 11.76:
                return Version.VERSION_HD
            return Version.VERSION_AOC
        elif version == 'VER 9.5':
            return Version.VERSION_AOFE21
        elif version == 'VER 9.8':
            return Version.VERSION_USERPATCH12
        elif version == 'VER 9.9':
            return Version.VERSION_USERPATCH13
        # UserPatch 1.4 RC 1
        elif version == 'VER 9.A':
            pass
        # UserPatch 1.4 RC 2
            pass
        elif version == 'VER 9.B' or version == 'VER 9.C' or version == 'VER 9.D':
            return Version.VERSION_USERPATCH14
        elif version == "VER 9.F":
            return Version.VERSION_USERPATCH15

        return version
