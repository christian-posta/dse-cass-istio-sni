# Datastax Cassandra with Istio and SNI routing

[Cassandra][cass] is a very popular "NoSQL" database. Cassandra is a highly distributed document database that can be tolerant to certain types of failures and scaled for data-intensive microservices. As Kubernetes has become the defacto container deployment platform for microservices, running stateful workloads like Cassandra is a common choice. There are quite a few guides showing how to [deploy Cassandra on Kubernetes as a StatefulSet][kube-stateful] but there are much fewer guides for connecting applications running outside of the Kubernetes cluster to the Cassandra database running inside the cluster. At Solo.io we help customers and prospects operationalize microservices networking and routing technology built on Envoy proxy like Gloo or Istio. In this blog post, we'll dig into the details of getting a deployment of Datastax Cassandra running on Kubernetes with TLS and SNI through Istio to enable routing from outside of the cluster.

We will take a step by step approach to this guide as the components themselves are quite complex. We will build up the architecture and consume the pieces as needed explaining the approach and benefits. As we are following a specific path in this blog, and there are many considerations and tradeoffs at each step, please do [reach out to us][contact] if you have questions or need help.

## The architecture for this blog

There are a few ways deploy Cassandra to Kubernetes and then use Istio to control the traffic routing. In this blog post, we're specifically considering the following architecture:

![](./img/Arch.png)

What we see in this architecture are the following salient points:

* Cassandra deployed with the [Datastax Cassandra Operator][cass-operator] as `StatefulSet`
* The Cassandra inter-node communication is secured with [TLS using Cassandra's configuration][cass-tls]
* Istio deployed as the service mesh treating the connections between the nodes as plaintext TCP
* Istio ingress gateway deployed at the edge with TLS passthrough and SNI routing configured
* Client lives outside the Kubernetes cluster with intent to connect to DB running inside cluster

In the following steps, we'll see the following sections:

* Deploying the Datastax Cassandra Kubernetes operator
* Deploy Istio 1.7.x
* Deploy a DSE `CassandraDatacenter` configured for TLS
* Configure Istio ingress for TCP routing
* Test Client
* Configure Istio for TLS passthrough/SNI routing
* Verify with client

## Source code for this blog

You can follow along or review the source code for this blog at the following repo:


# Deploying Datastax Cassandra

As mentioned previously, we'll be deploying Cassandra using the [Datastax Cassandra operator][cass-operator]. You can [read the official Datastax docs][official-dse-operator] for more details. We will specifically be installing the [DSE operator for Kubernetes 1.16][cass-operator-116]. 




[cass]: https://cassandra.apache.org
[kube-stateful]: https://kubernetes.io/docs/tutorials/stateful-application/cassandra/
[contact]: https://www.solo.io/company/contact/
[cass-operator]: https://github.com/datastax/cass-operator
[cass-tls]: https://docs.datastax.com/en/security/6.8/security/secSslTOC.html
[official-dse-operator]: https://docs.datastax.com/en/cass-operator/doc/cass-operator/cassOperatorAbout.html
[cass-operator-116]: https://github.com/datastax/cass-operator/tree/master/docs/user