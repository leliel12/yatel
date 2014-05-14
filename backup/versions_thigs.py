    def _is_version(self, obj):
        columns = {'comment': basestring, 'data': object,
                   'datetime': datetime.datetime,
                   'id': int, 'tag': basestring}
        is_version = True
        if isinstance(obj, dict) and len(obj) == len(columns) \
           and sorted(obj.keys()) == sorted(columns.keys()):
               for c, ct in columns.items():
                    if not isinstance(obj[c], ct):
                        is_version = False
                        break
        else:
            is_version = False
        return is_version


    def _row2version(self, row):
        ver = dict(row)
        if isinstance(row.data, basestring):
            ver["data"] = cPickle.loads(row.data)
        return ver


        # version dictionary
        elif self._is_version(elem):
            data = elem
            data.update(datetime=format_date(elem["datetime"]))
            tname = VERSIONS

        self.versions_table = sa.Table(
                VERSIONS, self._metadata,
                sa.Column("id", sa.Integer(), primary_key=True),
                sa.Column("tag", sa.String(512), unique=True, nullable=False),
                sa.Column("datetime", sa.DateTime(), nullable=False),
                sa.Column("comment", sa.Text(), nullable=False),
                sa.Column("data", sa.PickleType(), nullable=False),
            )

if not self.versions_count():
            self.save_version(tag="init", comment="-* AUTO CREATED *-")




    def versions_infos_interator(self):
        """A ``iterator`` with all existing versions.

        Each element contains 3 elements: the  version ``id``, the  version
        ``datetime`` of creation, and the  version ``tag``

        """
        query = sql.select([self.versions_table.c.id,
                            self.versions_table.c.datetime,
                            self.versions_table.c.tag])
        for row in self.execute(query):
            yield dict(row)

    def versions_iterator(self):
        """This function iterate over all versions

        WARNING: this is used only with dump propuses, use get_version for
        retrieve a particular version

        """
        query = sql.select([self.versions_table])
        for row in self.execute(query):
            yield self._row2version(row)

    def save_version(self, tag, comment="", hap_sql="",
                     topology={}, weight_range=(None, None), enviroments=()):
        """Store a new exploration status version in the database.

        **Params**
            :tag: The tag of the new version (unique).
            :comment: A comment about the new version.
            :hap_sql: For execute in ``YatelConnection.hap_sql``.
            :topology: A dictionary with hap_ids as keys and a *iterable*
                       with (x, y) position as value.
            :weight_tange: A *iterable* with two ``int`` or ``float``
                           representing the relevante ``dom.Edge`` instance.
            :enviroments: A *iterable* with 2 values: **1** a ``bool``
                          representing if the enviroment is active or not;
                          **2** A ``dict`` with ``dom.Fact`` attribute name
                          as keys, and attribute value as value.

        **Returns**
            A ``tuple`` with 3 values: the new version ``id``, the new version
            ``datetime`` of creation, and the new version ``tag``.

        """
        td = {}
        for hap_id, xy in topology.items():
            # validate if this hap is in this network
            self.haplotype_by_id(hap_id)
            td[hap_id] = list(xy)

        if not all(weight_range):
            weight_range = [e.weight for e in self.edges_min_and_max_weights()]
        minw, maxw = weight_range
        nwmin, nwmax = [e.weight for e in self.edges_min_and_max_weights()]
        if minw > maxw or minw < nwmin \
           or minw > nwmax or maxw > nwmax or maxw < nwmin:
            raise ValueError("Invalid range: ({}, {})".format(minw, maxw))
        wrl = [minw, maxw]

        envl = []
        for active, enviroment in enviroments:
            active = bool(active)
            for varname, varvalue in enviroment.items():
                if varname not in self.fact_attributes_names():
                    msg = "Invalid fact attribute: '{}'".format(varname)
                    raise ValueError(msg)
                if (varvalue is not None
                    and varvalue not in self.fact_attribute_values(varname)):
                        msg = "Invalid value '{}' for fact attribute '{}'"
                        msg = msg.format(varvalue, varname)
                        raise ValueError(msg)
            envl.append([active, enviroment])

        data = {"topology": td, "weight_range": wrl,
                "enviroments": envl, "hap_sql": hap_sql}

        try:
            old_data = self.get_version()["data"]
        except:
            pass
        else:
            if data == old_data:
                msg = "Nothing changed from the last version '{}'"
                msg = msg.format(vdbo.tag)
                raise ValueError(msg)

        query = sql.insert(self.versions_table).values(
            tag=tag, datetime=format_date(datetime.datetime.now()),
            comment=comment, data=data)
        self.execute(query)

    def get_version(self, match=None):
        """Return a version by the given filter.

        Behavior:
            * If ``match`` is ``None``: The last version is returned.
            * If ``match`` is instance of ``int``: The search is by version
              *id*.
            * If ``match`` is instance of ``datetime``: The search is by
              version creation *datetime*.
            * If ``match`` is instance of ``str``: The search is by version
              *tag*.

        """
        query = sql.select([self.versions_table])
        if match is None:
            query = query.order_by(self.versions_table.c.datetime.desc())
        elif isinstance(match, int):
            query = query.where(self.versions_table.c.id == match)
        elif isinstance(match, datetime.datetime):
            match = format_date(match)
            query = query.where(self.versions_table.c.datetime == match)
        elif isinstance(match, basestring):
            query = query.where(self.versions_table.c.tag == match)
        else:
            msg = "Match must be None, int, str, unicode or datetime instance"
            raise TypeError(msg)
        query = query.limit(1)
        row = self.execute(query).fetchone()
        return self._row2version(row)

    def versions_count(self):
        """Return how many versions are stored"""
        return len(
            tuple(self.execute(sql.select([self.versions_table.c.id])))
        )
