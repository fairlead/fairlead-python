from typing import TYPE_CHECKING, Any, Dict, List

from mataki._pagination import AsyncPage, SyncPage, _parse_async_page, _parse_sync_page
from mataki.types.ad import Ad, AdStatus, AdType
from mataki.types.line_item import BidderType, LineItem, LineItemStatus

if TYPE_CHECKING:
    from mataki._client import AsyncMataki, Mataki


class LineItemsResource:
    """Synchronous line items API."""

    def __init__(self, client: "Mataki") -> None:
        self._client = client

    def list(
        self,
        *,
        query: str | None = None,
        sort: str | None = None,
        offset: int = 0,
        limit: int = 25,
    ) -> SyncPage[LineItem]:
        """List line items with optional filtering, sorting, and pagination.

        Args:
            query: Filter expression (e.g. ``campaign_id = cmp_...``).
            sort: Sort clause (e.g. ``priority:desc``).
            offset: Number of items to skip.
            limit: Maximum items to return (1-100).

        Returns:
            A page of line items. Iterate directly to auto-paginate.
        """
        params = _list_params(query=query, sort=sort, offset=offset, limit=limit)
        response = self._client._request("GET", "/line-items", params=params)
        return _parse_sync_page(
            data=response.json(),
            client=self._client,
            path="/line-items",
            params=params,
            model=LineItem,
        )

    def get(self, entity_id: str) -> LineItem:
        """Get a line item by ID.

        Args:
            entity_id: Line item ID (e.g. ``li_4K7fR9pLm2nQwXvY8cJH3``).
        """
        response = self._client._request("GET", f"/line-items/{entity_id}")
        return LineItem.model_validate(response.json())

    def create(
        self,
        *,
        campaign_id: str,
        bid_strategy: str,
        bid_amount_cents: int,
        bidder_type: BidderType | str | None = None,
        status: LineItemStatus | str | None = None,
        targeting: Dict[str, object] | None = None,
        priority: int | None = None,
        delivery_goal: Dict[str, object] | None = None,
        tags: List[str] | None = None,
        labels: Dict[str, str] | None = None,
    ) -> LineItem:
        """Create a new line item.

        Args:
            campaign_id: Parent campaign ID.
            bid_strategy: Bidding strategy identifier.
            bid_amount_cents: Bid amount in cents.
            bidder_type: Bidder type (sponsored_listing). Defaults to sponsored_listing.
            status: Line item status (active, paused). Defaults to active.
            targeting: Targeting rules dictionary.
            priority: Priority level (higher = preferred). Defaults to 0.
            delivery_goal: Delivery goal configuration, or None.
            tags: Freeform tags for categorization.
            labels: Key-value labels for filtering.
        """
        body = _create_body(
            bid_strategy=bid_strategy,
            bid_amount_cents=bid_amount_cents,
            bidder_type=bidder_type,
            status=status,
            targeting=targeting,
            priority=priority,
            delivery_goal=delivery_goal,
            tags=tags,
            labels=labels,
        )
        response = self._client._request("POST", f"/campaigns/{campaign_id}/line-items", json=body)
        return LineItem.model_validate(response.json())

    def create_ad(
        self,
        line_item_id: str,
        *,
        ad_type: AdType | str,
        external_item_id: str | None = None,
        quality_score: float | str | None = None,
        metadata: Dict[str, object] | None = None,
        status: AdStatus | str | None = None,
        tags: List[str] | None = None,
        labels: Dict[str, str] | None = None,
    ) -> Ad:
        """Create a new ad under the specified line item.

        Args:
            line_item_id: Parent line item ID.
            ad_type: Ad format type (listing_ref, native, display).
            external_item_id: External item reference, or None.
            quality_score: Quality score (default "1.00").
            metadata: Arbitrary key-value metadata.
            status: Ad status (active, paused). Defaults to active.
            tags: Freeform tags for categorization.
            labels: Key-value labels for filtering.
        """
        body = _create_ad_body(
            ad_type=ad_type,
            external_item_id=external_item_id,
            quality_score=quality_score,
            metadata=metadata,
            status=status,
            tags=tags,
            labels=labels,
        )
        response = self._client._request("POST", f"/line-items/{line_item_id}/ads", json=body)
        return Ad.model_validate(response.json())

    def update(
        self,
        entity_id: str,
        *,
        bidder_type: BidderType | str | None = None,
        status: LineItemStatus | str | None = None,
        bid_strategy: str | None = None,
        bid_amount_cents: int | None = None,
        targeting: Dict[str, object] | None = None,
        priority: int | None = None,
        delivery_goal: Dict[str, object] | None = None,
        tags: List[str] | None = None,
        labels: Dict[str, str] | None = None,
    ) -> LineItem:
        """Update a line item. Only provided fields are changed.

        Args:
            entity_id: Line item ID.
            bidder_type: New bidder type, or None to leave unchanged.
            status: New status, or None to leave unchanged.
            bid_strategy: New bid strategy, or None to leave unchanged.
            bid_amount_cents: New bid amount in cents, or None to leave unchanged.
            targeting: New targeting rules, or None to leave unchanged.
            priority: New priority, or None to leave unchanged.
            delivery_goal: New delivery goal, or None to leave unchanged.
            tags: New tags, or None to leave unchanged.
            labels: New labels, or None to leave unchanged.
        """
        body = _update_body(
            bidder_type=bidder_type,
            status=status,
            bid_strategy=bid_strategy,
            bid_amount_cents=bid_amount_cents,
            targeting=targeting,
            priority=priority,
            delivery_goal=delivery_goal,
            tags=tags,
            labels=labels,
        )
        response = self._client._request("PATCH", f"/line-items/{entity_id}", json=body)
        return LineItem.model_validate(response.json())

    def delete(self, entity_id: str) -> None:
        """Delete a line item.

        Args:
            entity_id: Line item ID.
        """
        self._client._request("DELETE", f"/line-items/{entity_id}")


class AsyncLineItemsResource:
    """Asynchronous line items API."""

    def __init__(self, client: "AsyncMataki") -> None:
        self._client = client

    async def list(
        self,
        *,
        query: str | None = None,
        sort: str | None = None,
        offset: int = 0,
        limit: int = 25,
    ) -> AsyncPage[LineItem]:
        """List line items with optional filtering, sorting, and pagination.

        Args:
            query: Filter expression (e.g. ``campaign_id = cmp_...``).
            sort: Sort clause (e.g. ``priority:desc``).
            offset: Number of items to skip.
            limit: Maximum items to return (1-100).

        Returns:
            A page of line items. Async-iterate directly to auto-paginate.
        """
        params = _list_params(query=query, sort=sort, offset=offset, limit=limit)
        response = await self._client._request("GET", "/line-items", params=params)
        return _parse_async_page(
            data=response.json(),
            client=self._client,
            path="/line-items",
            params=params,
            model=LineItem,
        )

    async def get(self, entity_id: str) -> LineItem:
        """Get a line item by ID.

        Args:
            entity_id: Line item ID (e.g. ``li_4K7fR9pLm2nQwXvY8cJH3``).
        """
        response = await self._client._request("GET", f"/line-items/{entity_id}")
        return LineItem.model_validate(response.json())

    async def create(
        self,
        *,
        campaign_id: str,
        bid_strategy: str,
        bid_amount_cents: int,
        bidder_type: BidderType | str | None = None,
        status: LineItemStatus | str | None = None,
        targeting: Dict[str, object] | None = None,
        priority: int | None = None,
        delivery_goal: Dict[str, object] | None = None,
        tags: List[str] | None = None,
        labels: Dict[str, str] | None = None,
    ) -> LineItem:
        """Create a new line item.

        Args:
            campaign_id: Parent campaign ID.
            bid_strategy: Bidding strategy identifier.
            bid_amount_cents: Bid amount in cents.
            bidder_type: Bidder type (sponsored_listing). Defaults to sponsored_listing.
            status: Line item status (active, paused). Defaults to active.
            targeting: Targeting rules dictionary.
            priority: Priority level (higher = preferred). Defaults to 0.
            delivery_goal: Delivery goal configuration, or None.
            tags: Freeform tags for categorization.
            labels: Key-value labels for filtering.
        """
        body = _create_body(
            bid_strategy=bid_strategy,
            bid_amount_cents=bid_amount_cents,
            bidder_type=bidder_type,
            status=status,
            targeting=targeting,
            priority=priority,
            delivery_goal=delivery_goal,
            tags=tags,
            labels=labels,
        )
        response = await self._client._request("POST", f"/campaigns/{campaign_id}/line-items", json=body)
        return LineItem.model_validate(response.json())

    async def create_ad(
        self,
        line_item_id: str,
        *,
        ad_type: AdType | str,
        external_item_id: str | None = None,
        quality_score: float | str | None = None,
        metadata: Dict[str, object] | None = None,
        status: AdStatus | str | None = None,
        tags: List[str] | None = None,
        labels: Dict[str, str] | None = None,
    ) -> Ad:
        """Create a new ad under the specified line item.

        Args:
            line_item_id: Parent line item ID.
            ad_type: Ad format type (listing_ref, native, display).
            external_item_id: External item reference, or None.
            quality_score: Quality score (default "1.00").
            metadata: Arbitrary key-value metadata.
            status: Ad status (active, paused). Defaults to active.
            tags: Freeform tags for categorization.
            labels: Key-value labels for filtering.
        """
        body = _create_ad_body(
            ad_type=ad_type,
            external_item_id=external_item_id,
            quality_score=quality_score,
            metadata=metadata,
            status=status,
            tags=tags,
            labels=labels,
        )
        response = await self._client._request("POST", f"/line-items/{line_item_id}/ads", json=body)
        return Ad.model_validate(response.json())

    async def update(
        self,
        entity_id: str,
        *,
        bidder_type: BidderType | str | None = None,
        status: LineItemStatus | str | None = None,
        bid_strategy: str | None = None,
        bid_amount_cents: int | None = None,
        targeting: Dict[str, object] | None = None,
        priority: int | None = None,
        delivery_goal: Dict[str, object] | None = None,
        tags: List[str] | None = None,
        labels: Dict[str, str] | None = None,
    ) -> LineItem:
        """Update a line item. Only provided fields are changed.

        Args:
            entity_id: Line item ID.
            bidder_type: New bidder type, or None to leave unchanged.
            status: New status, or None to leave unchanged.
            bid_strategy: New bid strategy, or None to leave unchanged.
            bid_amount_cents: New bid amount in cents, or None to leave unchanged.
            targeting: New targeting rules, or None to leave unchanged.
            priority: New priority, or None to leave unchanged.
            delivery_goal: New delivery goal, or None to leave unchanged.
            tags: New tags, or None to leave unchanged.
            labels: New labels, or None to leave unchanged.
        """
        body = _update_body(
            bidder_type=bidder_type,
            status=status,
            bid_strategy=bid_strategy,
            bid_amount_cents=bid_amount_cents,
            targeting=targeting,
            priority=priority,
            delivery_goal=delivery_goal,
            tags=tags,
            labels=labels,
        )
        response = await self._client._request("PATCH", f"/line-items/{entity_id}", json=body)
        return LineItem.model_validate(response.json())

    async def delete(self, entity_id: str) -> None:
        """Delete a line item.

        Args:
            entity_id: Line item ID.
        """
        await self._client._request("DELETE", f"/line-items/{entity_id}")


# --- Private helpers ---


def _list_params(
    *,
    query: str | None,
    sort: str | None,
    offset: int,
    limit: int,
) -> dict[str, Any]:
    params: dict[str, Any] = {"offset": offset, "limit": limit}
    if query is not None:
        params["query"] = query
    if sort is not None:
        params["sort"] = sort
    return params


def _create_body(
    *,
    bid_strategy: str,
    bid_amount_cents: int,
    bidder_type: BidderType | str | None,
    status: LineItemStatus | str | None,
    targeting: dict[str, object] | None,
    priority: int | None,
    delivery_goal: dict[str, object] | None,
    tags: list[str] | None,
    labels: dict[str, str] | None,
) -> dict[str, Any]:
    body: dict[str, Any] = {
        "bid_strategy": bid_strategy,
        "bid_amount_cents": bid_amount_cents,
    }
    if bidder_type is not None:
        body["bidder_type"] = str(bidder_type)
    if status is not None:
        body["status"] = str(status)
    if targeting is not None:
        body["targeting"] = targeting
    if priority is not None:
        body["priority"] = priority
    if delivery_goal is not None:
        body["delivery_goal"] = delivery_goal
    if tags is not None:
        body["tags"] = tags
    if labels is not None:
        body["labels"] = labels
    return body


def _create_ad_body(
    *,
    ad_type: AdType | str,
    external_item_id: str | None,
    quality_score: float | str | None,
    metadata: dict[str, object] | None,
    status: AdStatus | str | None,
    tags: list[str] | None,
    labels: dict[str, str] | None,
) -> dict[str, Any]:
    body: dict[str, Any] = {
        "ad_type": str(ad_type),
    }
    if external_item_id is not None:
        body["external_item_id"] = external_item_id
    if quality_score is not None:
        body["quality_score"] = quality_score
    if metadata is not None:
        body["metadata"] = metadata
    if status is not None:
        body["status"] = str(status)
    if tags is not None:
        body["tags"] = tags
    if labels is not None:
        body["labels"] = labels
    return body


def _update_body(
    *,
    bidder_type: BidderType | str | None,
    status: LineItemStatus | str | None,
    bid_strategy: str | None,
    bid_amount_cents: int | None,
    targeting: dict[str, object] | None,
    priority: int | None,
    delivery_goal: dict[str, object] | None,
    tags: list[str] | None,
    labels: dict[str, str] | None,
) -> dict[str, Any]:
    body: dict[str, Any] = {}
    if bidder_type is not None:
        body["bidder_type"] = str(bidder_type)
    if status is not None:
        body["status"] = str(status)
    if bid_strategy is not None:
        body["bid_strategy"] = bid_strategy
    if bid_amount_cents is not None:
        body["bid_amount_cents"] = bid_amount_cents
    if targeting is not None:
        body["targeting"] = targeting
    if priority is not None:
        body["priority"] = priority
    if delivery_goal is not None:
        body["delivery_goal"] = delivery_goal
    if tags is not None:
        body["tags"] = tags
    if labels is not None:
        body["labels"] = labels
    return body
