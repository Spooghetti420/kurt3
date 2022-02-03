class MetaDataManager:
    def __init__(self, meta_json) -> None:
        self.semver = meta_json["semver"]
        self.vm = meta_json["vm"]
        self.user_agent = meta_json["agent"]

    # Re-serialize the metadata
    def output(self):
        return {
            "semver": self.semver,
            "vm": self.vm,
            "agent": self.user_agent
        }