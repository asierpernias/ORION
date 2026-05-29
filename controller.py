import threading

from ORION import run_orion, open_search


def controller_run_orion(self):

    if not self.lock.acquire(blocking=False):
        print("ORION is already running")
        return

  
    def task():

        try:

            result = run_orion(ui=None)

            print(result)

            if result:
                open_search(result["intent"])

        except Exception as e:

            print("Error:", e)

        finally:
            self.set_state(self.IDLE)
            self.lock.release()

    thread = threading.Thread(
        target=task,
        daemon=True
    )

    thread.start()