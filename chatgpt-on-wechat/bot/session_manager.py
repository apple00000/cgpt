from common.expired_dict import ExpiredDict
from common.log import logger
from config import conf

class Session(object):
    def __init__(self, session_id, system_prompt=None):
        self.session_id = session_id
        if system_prompt is None:
            self.system_prompt = conf().get("character_desc", "")
        else:
            self.system_prompt = system_prompt

    # set_system
    def set_system(self, system):
        raise NotImplementedError
    
    # add_system
    def add_system(self, system):
        raise NotImplementedError
    
    # 重置会话
    def reset(self):
        raise NotImplementedError

    def set_system_prompt(self, system_prompt):
        self.system_prompt = system_prompt
        # self.reset()

    def add_query(self, query):
        raise NotImplementedError

    def add_reply(self, reply):
        raise NotImplementedError
    
    def discard_exceeding(self, max_tokens=None, cur_tokens=None):
        raise NotImplementedError



class SessionManager(object):
    def __init__(self, sessioncls, **session_args):
        if conf().get('expires_in_seconds'):
            sessions = ExpiredDict(conf().get('expires_in_seconds'))
        else:
            sessions = dict()
        self.sessions = sessions
        self.sessioncls = sessioncls
        self.session_args = session_args

    def build_session(self, session_id, system_prompt=None):
        '''
            如果session_id不在sessions中，创建一个新的session并添加到sessions中
            如果system_prompt不会空，会更新session的system_prompt并重置session
        '''

        if session_id not in self.sessions:
            logger.info("xxx1 session_id {} init", session_id)
            self.sessions[session_id] = self.sessioncls(session_id, system_prompt, **self.session_args)
        # elif system_prompt is not None: # 如果有新的system_prompt，更新并重置session
            
        #     self.sessions[session_id] = self.sessioncls(session_id, system_prompt, **self.session_args)
        
        logger.info("xxx2 {}".format(system_prompt))
        self.sessions[session_id].set_system_prompt(system_prompt)

        logger.info("xxx3 {}".format(self.sessions[session_id]))

        session = self.sessions[session_id]
        return session
    
    # def build_session_multi(self, session_id, system_prompts):
    #     '''
    #         如果session_id不在sessions中，创建一个新的session并添加到sessions中
    #         如果system_prompt不会空，会更新session的system_prompt并重置session
    #     '''
    #     if session_id not in self.sessions:
    #         self.sessions[session_id] = self.sessioncls(session_id, system_prompts[0], **self.session_args)
    #         if len(system_prompts)>1:
    #             for i in range (1, len(system_prompts)):
    #                 self.sessions[session_id].add_system(system_prompts[i])
    #     else:
    #         for i in range (len(system_prompts)):
    #             self.sessions[session_id].add_system(system_prompts[i])
    #     session = self.sessions[session_id]
    #     return session
    
    def session_query(self, query, session_id):
        session = self.build_session(session_id)
        session.add_query(query)
        try:
            max_tokens = conf().get("conversation_max_tokens", 1000)
            total_tokens = session.discard_exceeding(max_tokens, None)
            logger.debug("prompt tokens used={}".format(total_tokens))
        except Exception as e:
            logger.debug("Exception when counting tokens precisely for prompt: {}".format(str(e)))
        return session
    
    def session_query_with_prompt(self, query, session_id, system_prompt):
        session = self.build_session(session_id, system_prompt)
        session.add_query(query)
        try:
            max_tokens = conf().get("conversation_max_tokens", 1000)
            total_tokens = session.discard_exceeding(max_tokens, None)
            logger.debug("prompt tokens used={}".format(total_tokens))
        except Exception as e:
            logger.debug("Exception when counting tokens precisely for prompt: {}".format(str(e)))
        return session

    def session_reply(self, reply, session_id, total_tokens = None):
        session = self.build_session(session_id)
        session.add_reply(reply)
        try:
            max_tokens = conf().get("conversation_max_tokens", 1000)
            tokens_cnt = session.discard_exceeding(max_tokens, total_tokens)
            logger.debug("raw total_tokens={}, savesession tokens={}".format(total_tokens, tokens_cnt))
        except Exception as e:
            logger.debug("Exception when counting tokens precisely for session: {}".format(str(e)))
        return session

    def clear_session(self, session_id):
        if session_id in self.sessions:
            del(self.sessions[session_id])

    def clear_all_session(self):
        self.sessions.clear()
