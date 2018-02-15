import logging
import ceph_manager

from tasks.ceph_test_case import wait_for_health
from teuthology.task import Task

log = logging.getLogger(__name__)


class CrushErrors(Task):

    def begin(self):
        cluster_name = self.ctx.managers.keys()[0]
        self.manager = self.ctx.managers[cluster_name]
        self.manager.mark_out_osd(0)
        self.manager.raw_cluster_cmd('osd', 'pool', 'create', 'crushtestpool', '128')
        log.info("waiting for crush errors warning")
        grace = 30
        wait_for_health(self.manager, "CRUSH_ERRORS", grace)
        self.manager.mark_in_osd(0)

task = CrushErrors
