from twitterapi import TwitterUIFlow

flow = TwitterUIFlow()


def login():
    flow.login_flow()
    flow.LoginJsInstrumentationSubtask()
    print(flow.get_subtask_ids())
    if "LoginEnterUserIdentifierSSO" in flow.get_subtask_ids():
        print("Telephone number / Email address / User name")
        flow.LoginEnterUserIdentifierSSO(input())
        print(flow.get_subtask_ids())
    if "LoginEnterAlternateIdentifierSubtask" in flow.get_subtask_ids():
        print(flow.content["subtasks"][0]["enter_text"]["primary_text"]["text"])
        flow.LoginEnterAlternateIdentifierSubtask(input())
        print(flow.get_subtask_ids())
    if "LoginEnterPassword" in flow.get_subtask_ids():
        print(flow.content["subtasks"][0]["enter_password"]["primary_text"]["text"])
        flow.LoginEnterPassword(input())
        print(flow.get_subtask_ids())
    if "AccountDuplicationCheck" in flow.get_subtask_ids():
        flow.AccountDuplicationCheck()
        print(flow.get_subtask_ids())
    if "LoginTwoFactorAuthChallenge" in flow.get_subtask_ids():
        print(
            flow.content["subtasks"][0]["enter_text"]["header"]["primary_text"]["text"]
        )
        flow.LoginTwoFactorAuthChallenge(input())
        print(flow.get_subtask_ids())
    if "LoginAcid" in flow.get_subtask_ids():
        print(
            flow.content["subtasks"][0]["enter_text"]["header"]["secondary_text"][
                "text"
            ]
        )
        flow.LoginAcid(input())
        print(flow.get_subtask_ids())
    if "LoginSuccessSubtask" in flow.get_subtask_ids():
        print("===========Success===========")
        print(flow.get_subtask_ids())
    if "SuccessExit" not in flow.get_subtask_ids():
        print("Error")
        exit()

    flow.SaveCookies("cookies.json")


if __name__ == "__main__":
    login()