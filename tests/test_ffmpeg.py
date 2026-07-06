from novadl.infrastructure.system.ffmpeg_checker import FFmpegChecker


class TestFFmpegChecker:
    def test_is_installed_returns_bool(self) -> None:
        result = FFmpegChecker.is_installed()
        assert isinstance(result, bool)

    def test_get_version_returns_string_or_none(self) -> None:
        version = FFmpegChecker.get_version()
        assert version is None or isinstance(version, str)

    def test_get_install_guide_returns_string(self) -> None:
        guide = FFmpegChecker.get_install_guide()
        assert isinstance(guide, str)
        assert "FFmpeg" in guide
