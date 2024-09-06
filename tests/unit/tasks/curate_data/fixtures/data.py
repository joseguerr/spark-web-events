INPUT_COLS = [
    "distinct_id",
    "device_id",
    "referring_domain",
    "current_url",
    "device",
    "event_processed_timestamp",
    "airbyte_emitted_at_timestamp",
    "_run_date",
]

INPUT_DATA = [
    ["1", "1", "abc.com", "url1", "device1", 1681304876983, 1681304876983, 20230412],
    [
        "1",
        "1",
        "abc.com",
        "url1",
        "device1",
        1681304876983,
        1681304876983,
        20230412,
    ],  # Duplicate
    ["2", "2", "opensea.io", "url2", "device2", 1681304876984, 1681304876984, 20230412],
    ["3", "3", "$direct", "url3", "device3", 1681304876985, 1681304876985, 20230412],
    ["4", "4", "abc.com", "url4", "device4", 1681304876986, 1681304876986, 20230412],
    ["5", "5", "opensea.io", "url5", "device5", 1681304876987, 1681304876987, 20230412],
    ["6", "6", "abc.com", "url6", "device6", 1681304876989, 1681304876989, 20230412],
    ["7", "7", "other.com", "url7", "device7", 1681304876992, 1681304876992, 20230412],
]

TEST_TRANSFORM_INPUT = [dict(zip(INPUT_COLS, row)) for row in INPUT_DATA]

TEST_TRANSFORM_OUTPUT_EXPECTED = [
    ["abc", 3, 1, 20230412],
    ["opensea", 2, 2, 20230412],
    ["direct traffic", 1, 3, 20230412],
    ["other", 1, 3, 20230412],
]
