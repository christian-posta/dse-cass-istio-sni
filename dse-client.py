#!/usr/bin/env python
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import logging
log = logging.getLogger()
log.setLevel("INFO")
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
log.addHandler(handler)
from os import environ as env
from cassandra import ConsistencyLevel
from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement
from cassandra.auth import PlainTextAuthProvider
from cassandra.connection import SniEndPointFactory, SniEndPoint
from ssl import SSLContext, PROTOCOL_TLS, CERT_REQUIRED
def main():
    #sniep = SniEndPoint(env.get("CQLSH_HOST"),env.get("CQLSH_PORT"))
    sniep = SniEndPoint(proxy_address=env.get("CQLSH_HOST"), server_name=env.get("CQLSH_HOST"), port=int(env.get("CQLSH_PORT")))
    ssl_context = SSLContext(PROTOCOL_TLS)
    ssl_context.load_verify_locations(env.get("SSL_CERTFILE"))
    ssl_context.verify_mode = CERT_REQUIRED
    ssl_context.check_hostname = False
    cluster = Cluster(
        ssl_context=ssl_context,
        auth_provider=PlainTextAuthProvider(username=env.get("CQL_USER"),
        password=env.get("CQL_PASSWORD")),
        contact_points=[sniep],
        endpoint_factory=SniEndPointFactory(env.get("CQLSH_HOST"),
        port=int(env.get("CQLSH_PORT"))))
    session = cluster.connect()
    future = session.execute_async("""
        select cluster_name, data_center from system.local;
        """ )
    #future = session.execute_async("""
    #    select * from system.peers;
    #    """ )
    log.info("key\tcol1\tcol2")
    log.info("---\t----\t----")
    try:
        rows = future.result()
    except Exception:
            log.exception("Error reading rows:")
            return
    for row in rows:
            log.info("got a row")
            log.info('\t'.join([str(x) for x in row]))
if __name__ == "__main__":
    main()