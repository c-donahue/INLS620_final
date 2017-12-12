This project lays out a basic design for a web service that allows the campus package center to integrate a locker pick up system.
The project contains two resources; the package inventory and individual packages. Users can input a package to the inventory
from the inventory resource, which then creates a new package resource as well. Both resources contain links to one another, and
both utilize forms in creating, updating, and deleting packages.

Each package resources includes a randomly generated id, the name of the recipient,the recipient's address, the time received, a locker
location (i.e "locker 20"), and an access code for the locker. The location and access code can be edited. See list below for full
explanation of data properties.

The microdata used for this service comes from schema.org, specically from the "Delivery Event" schema. Delivery event is a type of event,
which means the data revolves around actions and actors. While this may not be the ideal microdata type a real version of this web serivce,
it was the closest type on schema.org and is good enough for the needs of this project. Schema is located at http://schema.org/DeliveryEvent,
which actually has a subsection for Locker Delivery.

Data is in both microdata and RDFa format, as it was designed based on the html templates from the help ticket project.
----------------------------------------

Package Microdata Types and Properties

Name        Property            Type                            URL                             Description
_________________________________________________________________________________________________________________________________

package_id    Identifier       Property Value        http://schema.org/identifier          Used as unique identifier for each package

title          About            Thing                 http://schema.org/about              Title of entity is just "Package" + id. Defines
                                                                                           what the delivery event is about

recipient       Actor           Person                http://schema.org/actor              Name of person for whom the package is for. Because
                                                                                           this technically an event in the schema, the people
                                                                                           involved are technically "actors."

address        Location       Postal Address        http://schema.org/location             Postal address where package was ordered to.

time_received  availableFrom   DateTime            http://schema.org/availableFrom         Part of delivery event: the date time from which
                                                                                           the package is available from. Used in this case
                                                                                           to identify time received

location        Location        Place               http://schema.org/location             Part of delivery event: in this case used to denote
                                                                                           location of the package in the inventory, i.e the
                                                                                           locker number where the package is housed

access_code     accessCode      Text                http://schema.org/accessCode           Part of delivery event: a code used to access a package.
                                                                                           In this case the code corresponds to the locker in which
                                                                                           the package is housed. Used by recipient to retrieve

