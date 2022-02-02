class Project:

    pass
    """
        Properties:
            targets: list[Target]
                is_stage: bool
                name: str
                variables: dict[Variable]
                    {arbitrary unique identifier}: [
                        variable_name,
                        value
                    ], ...
                lists: dict[List]
                    {arbitrary unique identifier}: [
                        list_name,
                        [value1, value2, value3...]
                    ], ...
                broadcasts: dict[Broadcast]
                    {arbitrary unique identifier}: broadcast_name: str,
                blocks: dict[Block]:
                    {arbitrary unique identifier}: [
                        opcode: str,
                        next: str | null,
                        parent: str | null,
                        inputs: dict[Input]
                            ? (int),
                            [
                                ? (int),
                                value: str, (broadcast name here)
                                broadcast_id: str

                            ], ...
                        fields: ???,
                        shadow: bool,
                        topLevel: bool (appear or not),
                        x: float,
                        y: float
                    ]
                comments: dict[Comment]:
                    {arbitrary unique identifier}: 
                        blockId: str,
                        x: float,
                        y: float,
                        width: float,
                        height: float,
                        minimized: bool,
                        text: str
                current_costume: int,
                costumes: list[Costume]
                    assetId: str (md5 hash),
                    name: str,
                    md5ext: str (md5 hash + file extension),
                    dataFormat: str (file extension),
                    rotationCenterX: float,
                    rotationCenterY: float
                sounds: list[Sound]
                    assetId: str (md5 hash),
                    name: str,
                    dataFormat: str (file type),
                    format: "", ???
                    rate: int,
                    sampleCount: int,
                    md5ext: str (md5 + file extension)
                layerOrder: int

                volume: float
                <-- The stage (only) will have these properties: >
                tempo: float
                videoTransparency: float
                videoState: str ("on"/"off")
                textToSpeechLanguage: str (ISO language code, e.g. "ar")
                --------

                <-- Sprites will also have these properties: >
                visible: bool,
                x: float
                y: float
                size: float
                direction: float
                draggable: bool
                rotationStyle: str
            monitors: list[Monitor]
                id: variable/list's unique identifier
                mode: "list" | some others, e.g. default variable monitor display is "default"
                opcode: "data_variable" | "data_listcontents" 
                params: {
                    "LIST": str (name)
                }
                spriteName: null | str
                value: int | float | list | str
                width: float | int
                height: float | int
                x: float
                y: float
                visible: bool

                <-- Variable monitors in particular have the following as well: >
                sliderMin: float,
                sliderMax: float
                isDiscrete: bool
            extensions: list[str]
                e.g. "text2speech"
            meta: ProjectMetaData
                semver: "3.0.0",
                vm: "0.2.0-prerelease.20220118081555"
                agent: user agent here
    """