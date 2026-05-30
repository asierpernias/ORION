import threading
import time

from ORION import run_orion, open_search


def controller_run_orion(self):

    if not self.lock.acquire(blocking=False):
        print("ORION is already running")
        return

    def task():

        try:
            result = run_orion(ui=self)

            print(result)

            if result:
                engine = result["intent"].get("engine", "google")
                query = result["intent"].get("query", "")

                self.request_bubble(f"Abriendo {engine}: {query}")
                open_search(result["intent"])

                self.request_state(self.RESPONDING)
                time.sleep(1.5)

        except Exception as e:
            self.request_bubble("Ocurrio un error.")
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