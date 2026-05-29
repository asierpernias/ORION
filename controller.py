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
                open_search(result["intent"])

                self.request_state(self.RESPONDING)
                time.sleep(1.5)

        except Exception as e:
            print("Error:", e)

        finally:
            self.request_state(self.IDLE)
            self.lock.release()

    thread = threading.Thread(
        target=task,
        daemon=True
    )

    thread.start()