import threading
import time

from ORION import run_orion, open_search, run_text_command, OrionError


def controller_run_orion(self, text):

    if not self.lock.acquire(blocking=False):
        self.request_bubble("ORION is already running")
        return

    def task():

        try:
            self.request_state(self.SEARCHING)
            self.request_bubble("Procesando...")
            
            result = run_text_command(text, ui=self)

            print(result)

            if result:
                engine = result["intent"].get("engine", "google")
                query = result["intent"].get("query", "")

                self.request_bubble(f"Abriendo {engine}: {query}")
                open_search(result["intent"])

                self.request_state(self.RESPONDING)
                time.sleep(1.5)

        except OrionError as e:
            self.request_bubble(str(e))
            print("Orion error:", e)
            time.sleep(1.5)
        except Exception as e:
                self.request_bubble("Ocurrio un error inesperado.")
                print("Error:", e)
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

            print(result)

            if result:
                engine = result["intent"].get("engine", "google")
                query = result["intent"].get("query", "")

                self.request_bubble(f"Abriendo {engine}: {query}")

                open_search(result["intent"])

                self.request_state(self.RESPONDING)
                time.sleep(1.5)

        except OrionError as e:
            self.request_bubble(str(e))
            print("Orion error:", e)
            time.sleep(1.5)
        except Exception as e:
            self.request_bubble("Ocurrio un error inesperado.")
            print("Error:", e)
            time.sleep(1.5)
        finally:
            self.request_state(self.IDLE)
            self.lock.release()

    thread = threading.Thread(
        target=task,
        daemon=True
    )

    thread.start()