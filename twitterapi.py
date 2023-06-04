import os
from time import sleep
import requests
import json


class TwitterUIFlow:
    def __init__(
        self,
        proxies={},
        language="en",
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
    ):
        self.USER_AGENT = user_agent
        self.AUTHORIZATION = "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA"
        self.proxies = proxies
        self.session = requests.Session()
        if proxies is not {}:
            self.session.proxies = proxies
        self.__twitter()
        self.x_guest_token = self.__get_guest_token()
        self.method_check_bypass = False
        self.flow_token = None
        self.language = language
        self.mentions_cursor = None
        self.tweet_details_cusror = None
        self.tweet_entries = []

    def __twitter(self):
        headers = {
            "User-Agent": self.USER_AGENT,
        }
        response = self.session.get(
            "https://twitter.com/", headers=headers, proxies=self.proxies
        )
        return self

    def __get_guest_token(self):
        headers = {
            "authorization": self.AUTHORIZATION,
            "User-Agent": self.USER_AGENT,
        }
        response = self.session.post(
            "https://api.twitter.com/1.1/guest/activate.json",
            headers=headers,
            proxies=self.proxies,
        ).json()
        return response["guest_token"]

    def __get_headers(self):
        return {
            "authorization": self.AUTHORIZATION,
            "User-Agent": self.USER_AGENT,
            "Content-type": "application/json",
            "x-guest-token": self.x_guest_token,
            "x-csrf-token": self.session.cookies.get("ct0"),
            "x-twitter-active-user": "yes",
            "x-twitter-client-language": self.language,
            "origin": "https://twitter.com",
            "referer": "https://twitter.com/home",
        }

    def __get_media_upload_headers(self):
        return {
            "authorization": self.AUTHORIZATION,
            "User-Agent": self.USER_AGENT,
            "x-guest-token": self.x_guest_token,
            "x-csrf-token": self.session.cookies.get("ct0"),
            "x-twitter-active-user": "yes",
            "x-twitter-client-language": self.language,
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br",
            "origin": "https://twitter.com",
            "referer": "https://twitter.com/home",
        }

    def __get_headers_legacy(self):
        return {
            "authorization": self.AUTHORIZATION,
            "User-Agent": self.USER_AGENT,
            "Content-type": "application/x-www-form-urlencoded",
            "x-csrf-token": self.session.cookies.get("ct0"),
            "x-twitter-active-user": "yes",
            "x-twitter-auth-type": "OAuth2Session",
        }

    def get_subtask_ids(self):
        return [subtasks["subtask_id"] for subtasks in self.content["subtasks"]]

    def __flow_token_check(self):
        if self.flow_token == None:
            raise Exception("not found token")

    def __error_check(self):
        if self.content.get("errors"):
            raise Exception(self.content["errors"][0]["message"])

    def __method_check(self, method_name):
        if self.method_check_bypass:
            return
        if method_name not in self.get_subtask_ids():
            raise Exception(
                "{0} is inappropriate method. choose from {1}. information: https://github.com/satsshark/TwitterFlow#inappropriate-method".format(
                    method_name, ", ".join(self.get_subtask_ids())
                )
            )

    def LoadCookies(self, file_path):
        with open(file_path, "r") as f:
            for cookie in json.load(f):
                self.session.cookies.set_cookie(
                    requests.cookies.create_cookie(**cookie)
                )
        return self

    def SaveCookies(self, file_path):
        cookies = []
        for cookie in self.session.cookies:
            cookie_dict = dict(
                version=cookie.version,
                name=cookie.name,
                value=cookie.value,
                port=cookie.port,
                domain=cookie.domain,
                path=cookie.path,
                secure=cookie.secure,
                expires=cookie.expires,
                discard=cookie.discard,
                comment=cookie.comment,
                comment_url=cookie.comment_url,
                rfc2109=cookie.rfc2109,
                rest=cookie._rest,
            )
            cookies.append(cookie_dict)

        with open(file_path, "w") as f:
            json.dump(cookies, f, indent=4)
        return self

    def login_flow(self):
        data = {
            "input_flow_data": {
                "flow_context": {
                    "debug_overrides": {},
                    "start_location": {"location": "splash_screen"},
                }
            },
            "subtask_versions": {
                "contacts_live_sync_permission_prompt": 0,
                "email_verification": 1,
                "topics_selector": 1,
                "wait_spinner": 1,
                "cta": 4,
            },
        }
        params = {"flow_name": "login"}
        response = self.session.post(
            "https://twitter.com/i/api/1.1/onboarding/task.json",
            headers=self.__get_headers(),
            json=data,
            params=params,
            proxies=self.proxies,
        ).json()
        self.flow_token = response.get("flow_token")
        self.content = response
        self.__error_check()
        return self

    def LoginJsInstrumentationSubtask(self):
        self.__flow_token_check()
        self.__method_check("LoginJsInstrumentationSubtask")
        data = {
            "flow_token": self.flow_token,
            "subtask_inputs": [
                {
                    "subtask_id": "LoginJsInstrumentationSubtask",
                    "js_instrumentation": {
                        "response": json.dumps(
                            {
                                "rf": {
                                    "af07339bbc6d24ced887d705eb0c9fd29b4a7d7ddc21136c9f94d53a4bc774d2": 88,
                                    "a6ce87d6481c6ec4a823548be3343437888441d2a453061c54f8e2eb325856f7": 250,
                                    "a0062ad06384a8afd38a41cd83f31b0dbfdea0eff4b24c69f0dd9095b2fb56d6": 16,
                                    "a929e5913a5715d93491eaffaa139ba4977cbc826a5e2dbcdc81cae0f093db25": 186,
                                },
                                "s": "Q-H-53m1uXImK0F0ogrxRQtCWTH1KIlPbIy0MloowlMa4WNK5ZCcDoXyRs1q_cPbynK73w_wfHG_UVRKKBWRoh6UJtlPS5kMa1p8fEvTYi76hwdzBEzovieR8t86UpeSkSBFYcL8foYKSp6Nop5mQR_QHGyEeleclCPUvzS0HblBJqZZdtUo-6by4BgCyu3eQ4fY5nOF8fXC85mu6k34wo982LMK650NsoPL96DBuloqSZvSHU47wq2uA4xy24UnI2WOc6U9KTvxumtchSYNnXq1HV662B8U2-jWrzvIU4yUHV3JYUO6sbN6j8Ho9JaUNJpJSK7REwqCBQ3yG7iwMAAAAX2Vqcbs",
                            }
                        ),
                        "link": "next_link",
                    },
                }
            ],
        }
        response = self.session.post(
            "https://twitter.com/i/api/1.1/onboarding/task.json",
            headers=self.__get_headers(),
            json=data,
            proxies=self.proxies,
        ).json()
        self.flow_token = response.get("flow_token")
        self.content = response
        self.__error_check()
        return self

    def LoginEnterUserIdentifierSSO(self, user_id):
        self.__flow_token_check()
        self.__method_check("LoginEnterUserIdentifierSSO")
        data = {
            "flow_token": self.flow_token,
            "subtask_inputs": [
                {
                    "subtask_id": "LoginEnterUserIdentifierSSO",
                    "settings_list": {
                        "setting_responses": [
                            {
                                "key": "user_identifier",
                                "response_data": {"text_data": {"result": user_id}},
                            }
                        ],
                        "link": "next_link",
                    },
                }
            ],
        }
        response = self.session.post(
            "https://twitter.com/i/api/1.1/onboarding/task.json",
            headers=self.__get_headers(),
            json=data,
            proxies=self.proxies,
        ).json()
        self.flow_token = response.get("flow_token")
        self.content = response
        self.__error_check()
        return self

    def AccountDuplicationCheck(self):
        self.__flow_token_check()
        self.__method_check("AccountDuplicationCheck")
        data = {
            "flow_token": self.flow_token,
            "subtask_inputs": [
                {
                    "subtask_id": "AccountDuplicationCheck",
                    "check_logged_in_account": {
                        "link": "AccountDuplicationCheck_false"
                    },
                }
            ],
        }
        response = self.session.post(
            "https://twitter.com/i/api/1.1/onboarding/task.json",
            headers=self.__get_headers(),
            json=data,
            proxies=self.proxies,
        ).json()
        self.flow_token = response.get("flow_token")
        self.content = response
        self.__error_check()
        return self

    def LoginEnterAlternateIdentifierSubtask(self, text):
        self.__flow_token_check()
        self.__method_check("LoginEnterAlternateIdentifierSubtask")
        data = {
            "flow_token": self.flow_token,
            "subtask_inputs": [
                {
                    "subtask_id": "LoginEnterAlternateIdentifierSubtask",
                    "enter_text": {"text": text, "link": "next_link"},
                }
            ],
        }
        response = self.session.post(
            "https://twitter.com/i/api/1.1/onboarding/task.json",
            headers=self.__get_headers(),
            json=data,
            proxies=self.proxies,
        ).json()
        self.flow_token = response.get("flow_token")
        self.content = response
        self.__error_check()
        return self

    def LoginEnterPassword(self, password):
        self.__flow_token_check()
        self.__method_check("LoginEnterPassword")
        data = {
            "flow_token": self.flow_token,
            "subtask_inputs": [
                {
                    "subtask_id": "LoginEnterPassword",
                    "enter_password": {"password": password, "link": "next_link"},
                }
            ],
        }
        response = self.session.post(
            "https://twitter.com/i/api/1.1/onboarding/task.json",
            headers=self.__get_headers(),
            json=data,
            proxies=self.proxies,
        ).json()
        self.flow_token = response.get("flow_token")
        self.content = response
        self.__error_check()
        return self

    def LoginTwoFactorAuthChallenge(self, TwoFactorCode):
        self.__flow_token_check()
        self.__method_check("LoginTwoFactorAuthChallenge")
        data = {
            "flow_token": self.flow_token,
            "subtask_inputs": [
                {
                    "subtask_id": "LoginTwoFactorAuthChallenge",
                    "enter_text": {"text": TwoFactorCode, "link": "next_link"},
                }
            ],
        }
        response = self.session.post(
            "https://twitter.com/i/api/1.1/onboarding/task.json",
            headers=self.__get_headers(),
            json=data,
            proxies=self.proxies,
        ).json()
        self.flow_token = response.get("flow_token")
        self.content = response
        self.__error_check()
        return self

    def LoginAcid(self, acid):
        self.__flow_token_check()
        self.__method_check("LoginAcid")
        data = {
            "flow_token": self.flow_token,
            "subtask_inputs": [
                {
                    "subtask_id": "LoginAcid",
                    "enter_text": {"text": acid, "link": "next_link"},
                }
            ],
        }
        response = self.session.post(
            "https://twitter.com/i/api/1.1/onboarding/task.json",
            headers=self.__get_headers(),
            json=data,
            proxies=self.proxies,
        ).json()
        self.flow_token = response.get("flow_token")
        self.content = response
        self.__error_check()
        return self

    def get_att(self):
        data = {"flow_token": self.flow_token, "subtask_inputs": []}
        response = self.session.post(
            "https://twitter.com/i/api/1.1/onboarding/task.json",
            headers=self.__get_headers(),
            json=data,
            proxies=self.proxies,
        ).json()
        self.content = response
        self.__error_check()
        return self

    def Viewer(self):
        params = {
            "variables": json.dumps(
                {
                    "withCommunitiesMemberships": True,
                    "withCommunitiesCreation": True,
                    "withSuperFollowsUserFields": True,
                }
            )
        }
        response = self.session.get(
            "https://twitter.com/i/api/graphql/O_C5Q6xAVNOmeolcXjKqYw/Viewer",
            headers=self.__get_headers(),
            params=params,
            proxies=self.proxies,
        )

        self.content = response
        self.__error_check()
        return self

    def RedirectToPasswordReset(self):
        raise Exception(
            "RedirectToPasswordResetは現在サポートされていません。代わりにpassword_reset_flowを使用して下さい。"
        )

    def password_reset_flow(self):
        data = {
            "input_flow_data": {
                "flow_context": {
                    "debug_overrides": {},
                    "start_location": {"location": "manual_link"},
                }
            },
            "subtask_versions": {
                "contacts_live_sync_permission_prompt": 0,
                "email_verification": 1,
                "topics_selector": 1,
                "wait_spinner": 1,
                "cta": 4,
            },
        }
        params = {"flow_name": "password_reset"}
        response = self.session.post(
            "https://twitter.com/i/api/1.1/onboarding/task.json",
            headers=self.__get_headers(),
            json=data,
            params=params,
            proxies=self.proxies,
        ).json()
        self.flow_token = response.get("flow_token")
        self.content = response
        self.__error_check()
        return self

    def PwrJsInstrumentationSubtask(self):
        self.__flow_token_check()
        self.__method_check("PwrJsInstrumentationSubtask")
        data = {
            "flow_token": self.flow_token,
            "subtask_inputs": [
                {
                    "subtask_id": "PwrJsInstrumentationSubtask",
                    "js_instrumentation": {
                        "response": json.dumps(
                            {
                                "rf": {
                                    "af07339bbc6d24ced887d705eb0c9fd29b4a7d7ddc21136c9f94d53a4bc774d2": 88,
                                    "a6ce87d6481c6ec4a823548be3343437888441d2a453061c54f8e2eb325856f7": 250,
                                    "a0062ad06384a8afd38a41cd83f31b0dbfdea0eff4b24c69f0dd9095b2fb56d6": 16,
                                    "a929e5913a5715d93491eaffaa139ba4977cbc826a5e2dbcdc81cae0f093db25": 186,
                                },
                                "s": "Q-H-53m1uXImK0F0ogrxRQtCWTH1KIlPbIy0MloowlMa4WNK5ZCcDoXyRs1q_cPbynK73w_wfHG_UVRKKBWRoh6UJtlPS5kMa1p8fEvTYi76hwdzBEzovieR8t86UpeSkSBFYcL8foYKSp6Nop5mQR_QHGyEeleclCPUvzS0HblBJqZZdtUo-6by4BgCyu3eQ4fY5nOF8fXC85mu6k34wo982LMK650NsoPL96DBuloqSZvSHU47wq2uA4xy24UnI2WOc6U9KTvxumtchSYNnXq1HV662B8U2-jWrzvIU4yUHV3JYUO6sbN6j8Ho9JaUNJpJSK7REwqCBQ3yG7iwMAAAAX2Vqcbs",
                            }
                        ),
                        "link": "next_link",
                    },
                }
            ],
        }
        response = self.session.post(
            "https://twitter.com/i/api/1.1/onboarding/task.json",
            headers=self.__get_headers(),
            json=data,
            proxies=self.proxies,
        ).json()
        self.flow_token = response.get("flow_token")
        self.content = response
        self.__error_check()
        return self

    def PasswordResetBegin(self, user_id):
        self.__flow_token_check()
        self.__method_check("PasswordResetBegin")
        data = {
            "flow_token": self.flow_token,
            "subtask_inputs": [
                {
                    "subtask_id": "PasswordResetBegin",
                    "enter_text": {"text": user_id, "link": "next_link"},
                }
            ],
        }
        response = self.session.post(
            "https://twitter.com/i/api/1.1/onboarding/task.json",
            headers=self.__get_headers(),
            json=data,
            proxies=self.proxies,
        ).json()
        self.flow_token = response.get("flow_token")
        self.content = response
        self.__error_check()
        return self

    def PasswordResetChooseChallenge(self, choices="0"):
        self.__flow_token_check()
        self.__method_check("PasswordResetChooseChallenge")
        data = {
            "flow_token": self.flow_token,
            "subtask_inputs": [
                {
                    "subtask_id": "PasswordResetChooseChallenge",
                    "choice_selection": {
                        "link": "next_link",
                        "selected_choices": [choices],
                    },
                }
            ],
        }
        response = self.session.post(
            "https://twitter.com/i/api/1.1/onboarding/task.json",
            headers=self.__get_headers(),
            json=data,
            proxies=self.proxies,
        ).json()
        self.flow_token = response.get("flow_token")
        self.content = response
        self.__error_check()
        return self

    def PwrKnowledgeChallenge(self, text):
        self.__flow_token_check()
        self.__method_check("PwrKnowledgeChallenge")
        data = {
            "flow_token": self.flow_token,
            "subtask_inputs": [
                {
                    "subtask_id": "PwrKnowledgeChallenge",
                    "enter_text": {"text": text, "link": "next_link"},
                }
            ],
        }
        response = self.session.post(
            "https://twitter.com/i/api/1.1/onboarding/task.json",
            headers=self.__get_headers(),
            json=data,
            proxies=self.proxies,
        ).json()
        self.flow_token = response.get("flow_token")
        self.content = response
        self.__error_check()
        return self

    def PasswordResetConfirmChallenge(self, code):
        self.__flow_token_check()
        self.__method_check("PasswordResetConfirmChallenge")
        data = {
            "flow_token": self.flow_token,
            "subtask_inputs": [
                {
                    "subtask_id": "PasswordResetConfirmChallenge",
                    "enter_text": {"text": code, "link": "next_link"},
                }
            ],
        }
        response = self.session.post(
            "https://twitter.com/i/api/1.1/onboarding/task.json",
            headers=self.__get_headers(),
            json=data,
            proxies=self.proxies,
        ).json()
        self.flow_token = response.get("flow_token")
        self.content = response
        self.__error_check()
        return self

    def PasswordResetNewPassword(self, password):
        self.__flow_token_check()
        self.__method_check("PasswordResetNewPassword")
        data = {
            "flow_token": self.flow_token,
            "subtask_inputs": [
                {
                    "subtask_id": "PasswordResetNewPassword",
                    "enter_password": {"password": password, "link": "next_link"},
                }
            ],
        }
        response = self.session.post(
            "https://twitter.com/i/api/1.1/onboarding/task.json",
            headers=self.__get_headers(),
            json=data,
            proxies=self.proxies,
        ).json()
        self.flow_token = response.get("flow_token")
        self.content = response
        self.__error_check()
        return self

    def PasswordResetSurvey(self, choices="0"):
        self.__flow_token_check()
        self.__method_check("PasswordResetSurvey")
        data = {
            "flow_token": self.flow_token,
            "subtask_inputs": [
                {
                    "subtask_id": "PasswordResetSurvey",
                    "choice_selection": {
                        "link": "next_link",
                        "selected_choices": [choices],
                    },
                }
            ],
        }
        response = self.session.post(
            "https://twitter.com/i/api/1.1/onboarding/task.json",
            headers=self.__get_headers(),
            json=data,
            proxies=self.proxies,
        ).json()
        self.flow_token = response.get("flow_token")
        self.content = response
        self.__error_check()
        return self

    def CreateTweet(self, tweet_text, in_reply_to_tweet_id="0"):
        data = {
            "queryId": "XyvN0Wv13eeu_gVIHDi10g",
            "variables": json.dumps(
                {
                    "tweet_text": tweet_text,
                    "reply": {
                        "in_reply_to_tweet_id": in_reply_to_tweet_id,
                        "exclude_reply_user_ids": [],
                    },
                    "media": {"media_entities": [], "possibly_sensitive": False},
                    "withDownvotePerspective": False,
                    "withReactionsMetadata": False,
                    "withReactionsPerspective": False,
                    "withSuperFollowsTweetFields": True,
                    "withSuperFollowsUserFields": False,
                    "semantic_annotation_ids": [],
                    "dark_request": False,
                    "withBirdwatchPivots": False,
                }
            ),
        }
        response = self.session.post(
            "https://twitter.com/i/api/graphql/XyvN0Wv13eeu_gVIHDi10g/CreateTweet",
            headers=self.__get_headers(),
            json=data,
            proxies=self.proxies,
        ).json()
        self.content = response
        self.__error_check()
        return self

    def NoteTweet(self, tweet_text, in_reply_to_tweet_id="0"):
        data = {
            "queryId": "pwQhmvJv6I58pPtbjMzs2Q",
            "variables": json.dumps(
                {
                    "tweet_text": tweet_text,
                    "reply": {
                        "in_reply_to_tweet_id": in_reply_to_tweet_id,
                        "exclude_reply_user_ids": [],
                    },
                    "media": {"media_entities": [], "possibly_sensitive": False},
                    "semantic_annotation_ids": [],
                    "dark_request": False,
                }
            ),
            "features": json.dumps(
                {
                    "tweetypie_unmention_optimization_enabled": True,
                    "vibe_api_enabled": True,
                    "responsive_web_edit_tweet_api_enabled": True,
                    "graphql_is_translatable_rweb_tweet_is_translatable_enabled": True,
                    "view_counts_everywhere_api_enabled": True,
                    "longform_notetweets_consumption_enabled": True,
                    "tweet_awards_web_tipping_enabled": False,
                    "interactive_text_enabled": True,
                    "responsive_web_text_conversations_enabled": False,
                    "longform_notetweets_rich_text_read_enabled": True,
                    "longform_notetweets_inline_media_enabled": False,
                    "blue_business_profile_image_shape_enabled": True,
                    "responsive_web_graphql_exclude_directive_enabled": True,
                    "verified_phone_label_enabled": True,
                    "freedom_of_speech_not_reach_fetch_enabled": True,
                    "standardized_nudges_misinfo": True,
                    "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled": False,
                    "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
                    "responsive_web_graphql_timeline_navigation_enabled": True,
                    "responsive_web_enhance_cards_enabled": False,
                }
            ),
        }
        response = self.session.post(
            "https://twitter.com/i/api/graphql/pwQhmvJv6I58pPtbjMzs2Q/CreateNoteTweet",
            headers=self.__get_headers(),
            json=data,
            proxies=self.proxies,
        ).json()
        self.content = response
        self.__error_check()
        return self

    def FriendShipCheck(self, screen_name):
        params = {"variables": json.dumps({"screen_name": screen_name})}
        response = self.session.get(
            "https://api.twitter.com/graphql/9zwVLJ48lmVUk8u_Gh9DmA/ProfileSpotlightsQuery",
            headers=self.__get_headers(),
            params=params,
            proxies=self.proxies,
        ).json()
        self.content = response
        self.__error_check()
        return self

    def TweetDetails(self, tweetId):
        params = {
            "variables": json.dumps(
                {
                    "focalTweetId": tweetId,
                    "with_rux_injections": False,
                    "includePromotedContent": False,
                    "withCommunity": False,
                    "withQuickPromoteEligibilityTweetFields": False,
                    "withBirdwatchNotes": False,
                    "withVoice": False,
                    "withV2Timeline": True,
                    "withSuperFollowsUserFields": False,
                    "withDownvotePerspective": False,
                    "withReactionsMetadata": False,
                    "withReactionsPerspective": False,
                    "withSuperFollowsTweetFields": False,
                    "referrer": "profile",
                }
            ),
            "features": json.dumps(
                {
                    "rweb_lists_timeline_redesign_enabled": True,
                    "responsive_web_graphql_exclude_directive_enabled": True,
                    "verified_phone_label_enabled": True,
                    "creator_subscriptions_tweet_preview_api_enabled": True,
                    "responsive_web_graphql_timeline_navigation_enabled": True,
                    "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
                    "tweetypie_unmention_optimization_enabled": True,
                    "responsive_web_edit_tweet_api_enabled": True,
                    "graphql_is_translatable_rweb_tweet_is_translatable_enabled": True,
                    "view_counts_everywhere_api_enabled": True,
                    "longform_notetweets_consumption_enabled": True,
                    "tweet_awards_web_tipping_enabled": False,
                    "freedom_of_speech_not_reach_fetch_enabled": False,
                    "standardized_nudges_misinfo": True,
                    "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled": False,
                    "interactive_text_enabled": True,
                    "responsive_web_text_conversations_enabled": False,
                    "longform_notetweets_rich_text_read_enabled": True,
                    "longform_notetweets_inline_media_enabled": False,
                    "responsive_web_enhance_cards_enabled": False,
                    "responsive_web_twitter_blue_verified_badge_is_enabled": False,
                    "longform_notetweets_richtext_consumption_enabled": False,
                    "vibe_api_enabled": False,
                }
            ),
        }
        if self.tweet_details_cusror == None:
            response = self.session.get(
                "https://api.twitter.com/graphql/nDM-d-uWksu2D4Xj0Wl_Ig/TweetDetail",
                headers=self.__get_headers(),
                json=params,
                params=params,
                proxies=self.proxies,
            ).json()
            self.content = response
            self.__error_check()
            if "data" in response:
                if "threaded_conversation_with_injections_v2" in response["data"]:
                    if (
                        "instructions"
                        in response["data"]["threaded_conversation_with_injections_v2"]
                    ):
                        for instruction in response["data"][
                            "threaded_conversation_with_injections_v2"
                        ]["instructions"]:
                            if (
                                "entries" in instruction
                                and instruction["type"] == "TimelineAddEntries"
                            ):
                                self.tweet_entries = instruction["entries"]
                                for entry in instruction["entries"]:
                                    if entry["entryId"].startswith(
                                        "cursor-showmorethreads"
                                    ):
                                        self.tweet_details_cusror = entry["content"][
                                            "itemContent"
                                        ]["value"]
        else:
            params["cursor"] = self.tweet_details_cusror
            params["referrer"] = "tweet"
            response = self.session.get(
                "https://api.twitter.com/graphql/nDM-d-uWksu2D4Xj0Wl_Ig/TweetDetail",
                headers=self.__get_headers(),
                json=params,
                params=params,
                proxies=self.proxies,
            ).json()
            self.content = response
            self.__error_check()
            found_cursor = False
            if "data" in response:
                if "threaded_conversation_with_injections_v2" in response["data"]:
                    if (
                        "instructions"
                        in response["data"]["threaded_conversation_with_injections_v2"]
                    ):
                        for instruction in response["data"][
                            "threaded_conversation_with_injections_v2"
                        ]["instructions"]:
                            if (
                                "entries" in instruction
                                and instruction["type"] == "TimelineAddEntries"
                            ):
                                self.tweet_entries = (
                                    self.tweet_entries + instruction["entries"]
                                )
                                for entry in instruction["entries"]:
                                    if entry["entryId"].startswith(
                                        "cursor-showmorethreads"
                                    ) or entry["entryId"].startswith("cursor-bottom-"):
                                        self.tweet_details_cusror = entry["content"][
                                            "itemContent"
                                        ]["value"]
                                        found_cursor = True
            if found_cursor == False:
                self.tweet_details_cusror = None
        return self

    def FavoriteTweet(self, tweet_id):
        data = {
            "queryId": "lI07N6Otwv1PhnEgXILM7A",
            "variables": json.dumps(
                {
                    "tweet_id": tweet_id,
                }
            ),
        }
        response = self.session.post(
            "https://twitter.com/i/api/graphql/lI07N6Otwv1PhnEgXILM7A/FavoriteTweet",
            headers=self.__get_headers(),
            json=data,
            proxies=self.proxies,
        ).json()
        self.content = response
        self.__error_check()
        return self

    def UnfavoriteTweet(self, tweet_id):
        data = {
            "queryId": "ZYKSe-w7KEslx3JhSIk5LA",
            "variables": json.dumps(
                {
                    "tweet_id": tweet_id,
                }
            ),
        }
        response = self.session.post(
            "https://twitter.com/i/api/graphql/ZYKSe-w7KEslx3JhSIk5LA/UnfavoriteTweet",
            headers=self.__get_headers(),
            json=data,
            proxies=self.proxies,
        ).json()
        self.content = response
        self.__error_check()
        return self

    def CreateRetweet(self, tweet_id):
        data = {
            "queryId": "ojPdsZsimiJrUGLR1sjUtA",
            "variables": json.dumps(
                {
                    "tweet_id": tweet_id,
                    "dark_request": False,
                }
            ),
        }
        response = self.session.post(
            "https://twitter.com/i/api/graphql/ojPdsZsimiJrUGLR1sjUtA/CreateRetweet",
            headers=self.__get_headers(),
            json=data,
            proxies=self.proxies,
        ).json()
        self.content = response
        self.__error_check()
        return self

    def DeleteRetweet(self, tweet_id):
        data = {
            "queryId": "iQtK4dl5hBmXewYZuEOKVw",
            "variables": json.dumps(
                {
                    "source_tweet_id": tweet_id,
                    "dark_request": False,
                }
            ),
        }
        response = self.session.post(
            "https://twitter.com/i/api/graphql/iQtK4dl5hBmXewYZuEOKVw/DeleteRetweet",
            headers=self.__get_headers(),
            json=data,
            proxies=self.proxies,
        ).json()
        self.content = response
        self.__error_check()
        return self

    def friendships_create(self, tweet_id):
        data = {
            "include_profile_interstitial_type": 1,
            "include_blocking": 1,
            "include_blocked_by": 1,
            "include_followed_by": 1,
            "include_want_retweets": 1,
            "include_mute_edge": 1,
            "include_can_dm": 1,
            "include_can_media_tag": 1,
            "include_ext_has_nft_avatar": 1,
            "skip_status": 1,
            "id": tweet_id,
        }
        response = self.session.post(
            "https://twitter.com/i/api/1.1/friendships/create.json",
            headers=self.__get_headers_legacy(),
            data=data,
            proxies=self.proxies,
        ).json()
        self.content = response
        return self

    def friendships_destroy(self, tweet_id):
        data = {
            "include_profile_interstitial_type": 1,
            "include_blocking": 1,
            "include_blocked_by": 1,
            "include_followed_by": 1,
            "include_want_retweets": 1,
            "include_mute_edge": 1,
            "include_can_dm": 1,
            "include_can_media_tag": 1,
            "include_ext_has_nft_avatar": 1,
            "skip_status": 1,
            "id": tweet_id,
        }
        response = self.session.post(
            "https://twitter.com/i/api/1.1/friendships/destroy.json",
            headers=self.__get_headers_legacy(),
            data=data,
            proxies=self.proxies,
        ).json()
        self.content = response
        return self

    def getMentions(self, count=40):
        params = {
            "include_profile_interstitial_type": 1,
            "include_blocking": 1,
            "include_blocked_by": 1,
            "include_followed_by": 1,
            "include_want_retweets": 1,
            "include_mute_edge": 1,
            "include_can_dm": 1,
            "include_can_media_tag": 1,
            "include_ext_has_nft_avatar": 1,
            "include_ext_is_blue_verified": 1,
            "include_ext_verified_type": 1,
            "include_ext_profile_image_shape": 1,
            "skip_status": 1,
            "cards_platform": "Web-12",
            "include_cards": 1,
            "include_ext_alt_text": True,
            "include_ext_limited_action_results": False,
            "include_quote_count": True,
            "include_reply_count": 1,
            "tweet_mode": "extended",
            "include_ext_views": True,
            "include_entities": True,
            "include_user_entities": True,
            "include_ext_media_color": True,
            "include_ext_media_availability": True,
            "include_ext_sensitive_media_warning": True,
            "include_ext_trusted_friends_metadata": True,
            "send_error_codes": True,
            "simple_quoted_tweet": True,
            "count": count,
            "requestContext": "launch",
            "ext": "mediaStats,highlightedLabel,hasNftAvatar,voiceInfo,birdwatchPivot,enrichments,superFollowMetadata,unmentionInfo,editControl,vibe",
        }
        if self.mentions_cursor != None:
            params["cursor"] = self.mentions_cursor
        response = self.session.get(
            "https://twitter.com/i/api/2/notifications/mentions.json",
            headers=self.__get_headers(),
            params=params,
            proxies=self.proxies,
        ).json()
        self.content = response
        self.__error_check()
        for instruction in response["timeline"]["instructions"]:
            if "addEntries" in instruction:
                for entry in instruction["addEntries"]["entries"]:
                    if entry["entryId"].startswith("cursor-top-"):
                        self.mentions_cursor = entry["content"]["operation"][
                            "cursor"
                        ]["value"]
        return self

