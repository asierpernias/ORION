import threading
import time

from ORION import run_orion, run_text_command, OrionError
from i18n import t

import logging

def controller_run_orion(self):

    if not self.lock.acquire(blocking=False):
        self.request_bubble(t("already_running"))
        return

    def task():

        try:
            self.request_state(self.SEARCHING)
            self.request_bubble(t("processing"))
            
            result = run_orion(ui=self)

            logging.debug(result)

            if result:
                time.sleep(3)
                self.request_state(self.RESPONDING)
                time.sleep(1.5)

        except OrionError as e:
            self.request_bubble(str(e))
            logging.error("Orion error:", e)
            time.sleep(1.5)
        except Exception as e:
                self.request_bubble(t("unexpected"))
                logging.error("Error:", e)
                time.sleep(1.5)
        finally:
            self.request_state(self.IDLE)
            self.lock.release()

    thread = threading.Thread(
        target=task,
        daemon=True
    )

    thread.start()

def controller_run_text(self, text):

    if not self.lock.acquire(blocking=False):
        self.request_bubble("ORION is already running")
        return

    def task():

        try:
            self.request_state(self.SEARCHING)
            self.request_bubble("Procesando...")

            result = run_text_command(text, ui=self)

            logging.debug(result)

            if result:
                
                time.sleep(1.5)

        except OrionError as e:
            self.request_bubble(str(e))
            logging.error("Orion error:", e)
            time.sleep(1.5)
        except Exception as e:
            self.request_bubble("Ocurrio un error inesperado.")
            logging.error("Error:", e)
            time.sleep(1.5)
        finally:
            self.request_state(self.IDLE)
            self.lock.release()

    thread = threading.Thread(
        target=task,
        daemon=True
    )

    thread.start()