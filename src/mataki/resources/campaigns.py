from typing import TYPE_CHECKING, Any, Dict, List

from mataki._pagination import AsyncPage, SyncPage, _parse_async_page, _parse_sync_page
from mataki.types.campaign import Campaign, CampaignStatus
from mataki.types.line_item import BidderType, LineItem, LineItemStatus

if TYPE_CHECKING:
    from mataki._client import AsyncMataki, Mataki


class CampaignsResource:
    """Synchronous campaigns API."""

    def __init__(self, client: "Mataki") -> None:
        self._client = client

    def list(
        self,
        *,
        query: str | None = None,
        sort: str | None = None,
        offset: int = 0,
        limit: int = 25,
    ) -> SyncPage[Campaign]:
        """List campaigns with optional filtering, sorting, and pagination.

        Args:
            query: Filter expression (e.g. ``advertiser_id = adv_...``).
            sort: Sort clause (e.g. ``name:asc``).
            offset: Number of items to skip.
            limit: Maximum items to return (1-100).

        Returns:
            A page of campaigns. Iterate directly to auto-paginate.
        """
        params = _list_params(query=query, sort=sort, offset=offset, limit=limit)
        response = self._client._request("GET", "/campaigns", params=params)
        return _parse_sync_page(
            data=response.json(),
            client=self._client,
            path="/campaigns",
            params=params,
            model=Campaign,
        )

    def get(self, entity_id: str) -> Campaign:
        """Get a campaign by ID.

        Args:
            entity_id: Campaign ID (e.g. ``cmp_4K7fR9pLm2nQwXvY8cJH3``).
        """
        response = self._client._request("GET", f"/campaigns/{entity_id}")
        return Campaign.model_validate(response.json())

    def create(
        self,
        *,
        advertiser_id: str,
        name: str,
        status: CampaignStatus | str | None = None,
        budget_total_cents: int | None = None,
        budget_daily_cents: int | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
        tags: List[str] | None = None,
        labels: Dict[str, str] | None = None,
    ) -> Campaign:
        """Create a new campaign.

        Args:
            advertiser_id: Parent advertiser ID.
            name: Display name (1-255 characters).
            status: Campaign status (draft, active, paused, completed). Defaults to draft.
            budget_total_cents: Total budget in cents, or None for unlimited.
            budget_daily_cents: Daily budget in cents, or None for unlimited.
            start_date: Campaign start date (YYYY-MM-DD), or None.
            end_date: Campaign end date (YYYY-MM-DD), or None.
            tags: Freeform tags for categorization.
            labels: Key-value labels for filtering.
        """
        body = _create_body(
            advertiser_id=advertiser_id,
            name=name,
            status=status,
            budget_total_cents=budget_total_cents,
            budget_daily_cents=budget_daily_cents,
            start_date=start_date,
            end_date=end_date,
            tags=tags,
            labels=labels,
        )
        response = self._client._request("POST", "/campaigns", json=body)
        return Campaign.model_validate(response.json())

    def create_line_item(
        self,
        campaign_id: str,
        *,
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
        """Create a new line item under the specified campaign.

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
        body = _create_line_item_body(
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

    def update(
        self,
        entity_id: str,
        *,
        name: str | None = None,
        status: CampaignStatus | str | None = None,
        budget_total_cents: int | None = None,
        budget_daily_cents: int | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
        tags: List[str] | None = None,
        labels: Dict[str, str] | None = None,
    ) -> Campaign:
        """Update a campaign. Only provided fields are changed.

        Args:
            entity_id: Campaign ID.
            name: New display name, or None to leave unchanged.
            status: New status, or None to leave unchanged.
            budget_total_cents: New total budget in cents, or None to leave unchanged.
            budget_daily_cents: New daily budget in cents, or None to leave unchanged.
            start_date: New start date, or None to leave unchanged.
            end_date: New end date, or None to leave unchanged.
            tags: New tags, or None to leave unchanged.
            labels: New labels, or None to leave unchanged.
        """
        body = _update_body(
            name=name,
            status=status,
            budget_total_cents=budget_total_cents,
            budget_daily_cents=budget_daily_cents,
            start_date=start_date,
            end_date=end_date,
            tags=tags,
            labels=labels,
        )
        response = self._client._request("PATCH", f"/campaigns/{entity_id}", json=body)
        return Campaign.model_validate(response.json())

    def delete(self, entity_id: str) -> None:
        """Delete a campaign.

        Args:
            entity_id: Campaign ID.
        """
        self._client._request("DELETE", f"/campaigns/{entity_id}")


class AsyncCampaignsResource:
    """Asynchronous campaigns API."""

    def __init__(self, client: "AsyncMataki") -> None:
        self._client = client

    async def list(
        self,
        *,
        query: str | None = None,
        sort: str | None = None,
        offset: int = 0,
        limit: int = 25,
    ) -> AsyncPage[Campaign]:
        """List campaigns with optional filtering, sorting, and pagination.

        Args:
            query: Filter expression (e.g. ``advertiser_id = adv_...``).
            sort: Sort clause (e.g. ``name:asc``).
            offset: Number of items to skip.
            limit: Maximum items to return (1-100).

        Returns:
            A page of campaigns. Async-iterate directly to auto-paginate.
        """
        params = _list_params(query=query, sort=sort, offset=offset, limit=limit)
        response = await self._client._request("GET", "/campaigns", params=params)
        return _parse_async_page(
            data=response.json(),
            client=self._client,
            path="/campaigns",
            params=params,
            model=Campaign,
        )

    async def get(self, entity_id: str) -> Campaign:
        """Get a campaign by ID.

        Args:
            entity_id: Campaign ID (e.g. ``cmp_4K7fR9pLm2nQwXvY8cJH3``).
        """
        response = await self._client._request("GET", f"/campaigns/{entity_id}")
        return Campaign.model_validate(response.json())

    async def create(
        self,
        *,
        advertiser_id: str,
        name: str,
        status: CampaignStatus | str | None = None,
        budget_total_cents: int | None = None,
        budget_daily_cents: int | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
        tags: List[str] | None = None,
        labels: Dict[str, str] | None = None,
    ) -> Campaign:
        """Create a new campaign.

        Args:
            advertiser_id: Parent advertiser ID.
            name: Display name (1-255 characters).
            status: Campaign status (draft, active, paused, completed). Defaults to draft.
            budget_total_cents: Total budget in cents, or None for unlimited.
            budget_daily_cents: Daily budget in cents, or None for unlimited.
            start_date: Campaign start date (YYYY-MM-DD), or None.
            end_date: Campaign end date (YYYY-MM-DD), or None.
            tags: Freeform tags for categorization.
            labels: Key-value labels for filtering.
        """
        body = _create_body(
            advertiser_id=advertiser_id,
            name=name,
            status=status,
            budget_total_cents=budget_total_cents,
            budget_daily_cents=budget_daily_cents,
            start_date=start_date,
            end_date=end_date,
            tags=tags,
            labels=labels,
        )
        response = await self._client._request("POST", "/campaigns", json=body)
        return Campaign.model_validate(response.json())

    async def create_line_item(
        self,
        campaign_id: str,
        *,
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
        """Create a new line item under the specified campaign.

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
        body = _create_line_item_body(
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

    async def update(
        self,
        entity_id: str,
        *,
        name: str | None = None,
        status: CampaignStatus | str | None = None,
        budget_total_cents: int | None = None,
        budget_daily_cents: int | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
        tags: List[str] | None = None,
        labels: Dict[str, str] | None = None,
    ) -> Campaign:
        """Update a campaign. Only provided fields are changed.

        Args:
            entity_id: Campaign ID.
            name: New display name, or None to leave unchanged.
            status: New status, or None to leave unchanged.
            budget_total_cents: New total budget in cents, or None to leave unchanged.
            budget_daily_cents: New daily budget in cents, or None to leave unchanged.
            start_date: New start date, or None to leave unchanged.
            end_date: New end date, or None to leave unchanged.
            tags: New tags, or None to leave unchanged.
            labels: New labels, or None to leave unchanged.
        """
        body = _update_body(
            name=name,
            status=status,
            budget_total_cents=budget_total_cents,
            budget_daily_cents=budget_daily_cents,
            start_date=start_date,
            end_date=end_date,
            tags=tags,
            labels=labels,
        )
        response = await self._client._request("PATCH", f"/campaigns/{entity_id}", json=body)
        return Campaign.model_validate(response.json())

    async def delete(self, entity_id: str) -> None:
        """Delete a campaign.

        Args:
            entity_id: Campaign ID.
        """
        await self._client._request("DELETE", f"/campaigns/{entity_id}")


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
    advertiser_id: str,
    name: str,
    status: CampaignStatus | str | None,
    budget_total_cents: int | None,
    budget_daily_cents: int | None,
    start_date: str | None,
    end_date: str | None,
    tags: list[str] | None,
    labels: dict[str, str] | None,
) -> dict[str, Any]:
    body: dict[str, Any] = {"advertiser_id": advertiser_id, "name": name}
    if status is not None:
        body["status"] = str(status)
    if budget_total_cents is not None:
        body["budget_total_cents"] = budget_total_cents
    if budget_daily_cents is not None:
        body["budget_daily_cents"] = budget_daily_cents
    if start_date is not None:
        body["start_date"] = start_date
    if end_date is not None:
        body["end_date"] = end_date
    if tags is not None:
        body["tags"] = tags
    if labels is not None:
        body["labels"] = labels
    return body


def _create_line_item_body(
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


def _update_body(
    *,
    name: str | None,
    status: CampaignStatus | str | None,
    budget_total_cents: int | None,
    budget_daily_cents: int | None,
    start_date: str | None,
    end_date: str | None,
    tags: list[str] | None,
    labels: dict[str, str] | None,
) -> dict[str, Any]:
    body: dict[str, Any] = {}
    if name is not None:
        body["name"] = name
    if status is not None:
        body["status"] = str(status)
    if budget_total_cents is not None:
        body["budget_total_cents"] = budget_total_cents
    if budget_daily_cents is not None:
        body["budget_daily_cents"] = budget_daily_cents
    if start_date is not None:
        body["start_date"] = start_date
    if end_date is not None:
        body["end_date"] = end_date
    if tags is not None:
        body["tags"] = tags
    if labels is not None:
        body["labels"] = labels
    return body
