TEST_TRANSFORM_INPUT = [
    {
        "_airbyte_emitted_at": "1681304876983",
        "_airbyte_data": {
            "referring_domain": "abc.com",
            "distinct_id": "1877594018a86b-056670b0d7f6d28-7e7c3061-60c28-1877594018b295b",
            "device_id": "1877594018a86b-056670b0d7f6d28-7e7c3061-60c28-1877594018b295b",
            "device": "iPhone",
            "current_url": "https://us.myshop.com/item/40",
            "processed_time": "1681304876983"
        }
    }
]

TEST_TRANSFORM_OUTPUT_EXPECTED = [
    {
        "distinct_id": "1877594018a86b-056670b0d7f6d28-7e7c3061-60c28-1877594018b295b",
        "device_id": "1877594018a86b-056670b0d7f6d28-7e7c3061-60c28-1877594018b295b",
        "referring_domain": "abc.com",
        "current_url": "https://us.myshop.com/item/40",
        "device": "iPhone",
        "event_processed_timestamp": 1681304876983,
        "airbyte_emitted_at_timestamp": 1681304876983,
        "_run_date": 20230412
    }
]
