from channels_profile import Profile

message_recipient = 'nub_mirror'
source_channels = {
    'it_job_ua',
    'recruitingUA',
    'nub_general',
    '+uvTg8_sOV8gzYTBi',
    'djinni_official',
    'itua_python',
    'LvivPyVacancies'
}

instance = Profile('recruitment', message_recipient, source_channels)
